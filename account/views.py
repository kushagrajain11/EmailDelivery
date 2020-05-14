from django.shortcuts import render
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.shortcuts import render, get_object_or_404, redirect, redirect
from django.http import HttpResponse
from django.views.decorators.http import require_GET, require_POST,require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.core.urlresolvers import reverse
from django.conf import settings
from django.contrib.auth.decorators import login_required
from .import models, forms
from django.template import loader
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.http import JsonResponse
from account import models as AccountModels
from mail import models as MailModels
from django.template import Context, Template


@require_http_methods(['GET', 'POST'])
@login_required
def home(request, id):
	r = AccountModels.MyUser.objects.get(userID = id)
	context = {'r' : r.receivedMessages.all().order_by('-dateTime')}
	return HttpResponse(render(request, 'account/logged_in.html', context))


@require_http_methods(['GET', 'POST'])
def login(request):
	if request.user.is_authenticated():
		return redirect(reverse('home', kwargs = {'id' : request.user.userID}))

	if request.method == 'GET':
		f = forms.LoginForm()
		return HttpResponse(render(request, 'account/login.html', {'f' : f}))

	f = forms.LoginForm(request.POST)

	if not f.is_valid():
		return HttpResponse(render(request, 'account/login.html', {'f' : f}))

	username = request.POST.get('username')
	password = request.POST.get('password')
	user = authenticate(username = username, password = password)

	if not user:
		return HttpResponse(render(request, 'account/login.html', {'f' : f}))

	if not user.is_active:
		return HttpResponse(render(request, 'account/login.html', {'f' : forms.LoginForm(), 'message' : 'verify your email first.'}))

	auth_login(request, user)
	return redirect(reverse('home', kwargs = {'id' : user.userID}))


@require_http_methods(['GET', 'POST'])
def forgotPassword(request):
	if request.user.is_authenticated():
		return redirect(reverse('home', kwargs = {'id' : request.user.userID}))

	if request.method == 'GET':
		return HttpResponse(render(request, 'account/forgotPassword.html', {'f' : forms.ForgotPasswordForm}))

	f = forms.ForgotPasswordForm(request.POST)

	if not f.is_valid():
		return HttpResponse(render(request, 'account/forgotPassword.html', {'f' : f}))

	targetUser = models.MyUser.objects.filter(username = request.POST.get('username'))[0]
	recipient_email = targetUser.email
	sender = settings.EMAIL_HOST_USER
	subject = 'Forgot Password On Our Website.'

	code = models.createOTP(targetUser, 'FP')
	link = 'localhost:8000/account/confirm/' +  str(targetUser.userID) + '/' + str(code)

	text_message = loader.render_to_string('account/sentMail-fp.html', {'link' : link})
	message = EmailMultiAlternatives(subject, text_message, sender, [recipient_email])
	message.send()
	string = "An email has been sent to you on '" + recipient_email + "' for recovery. Follow the link received to reset your password."
	return HttpResponse(render(request, 'common/success_NotLoggedIn.html', {'message' : string}))


@require_http_methods(['GET', 'POST'])
def confirm(request, userID, otp):
	if request.user.is_authenticated():
		return redirect(reverse('home', kwargs = {'id' : request.user.userID}))

	if request.method == 'GET':
		user = models.MyUser.objects.get(userID = userID)
		if not user:
			return HttpResponse('No such user')

		otp_object = models.OTP.objects.get(code = otp, user = user)
		if not otp_object:
			return HttpResponse('Invalid credentials.')

		purpose = otp_object.purpose

		if purpose == 'FP':
			f = forms.ResetPasswordForm()
			return HttpResponse(render(request, 'account/resetPassword.html', {'f' : f, 'userID' : userID, 'otp' : otp}))

		else:
			userObject = models.MyUser.objects.get(userID = userID)
			userObject.is_active = True
			userObject.save()
			otp_object.delete()
			string = 'You have successfully completed the signup process.'
			return HttpResponse(render(request, 'common/success.html', {'message' : string}))

	else:
		f = forms.ResetPasswordForm(request.POST)

		if not f.is_valid():
			return HttpResponse(render(request, 'account/resetPassword.html', {'f' : f, 'userID' : userID, 'otp' : otp}))		

		userObject = models.MyUser.objects.get(userID = userID)
		userObject.set_password(request.POST.get('newPassword'))
		userObject.save()

		user = models.MyUser.objects.get(userID = userID)
		otp_object = models.OTP.objects.get(code = otp, user = user)
		otp_object.delete()
		string = 'Your password has been updated successfully.'
		return HttpResponse(render(request, 'common/success_NotLoggedIn.html', {'message' : string}))


@require_http_methods(['GET', 'POST'])
def signup(request):
	if request.user.is_authenticated():
		return redirect(reverse('home', kwargs = {'id' : request.user.userID}))

	if request.method == 'GET':
		return HttpResponse(render(request, 'account/signup.html', {'f' : forms.SignupForm()}))

	f = forms.SignupForm(request.POST)

	if not f.is_valid():
		return HttpResponse(render(request, 'account/signup.html', {'f' : f}))

	username 	= f.cleaned_data['username']
	password 	= f.cleaned_data['password']
	email 		= f.cleaned_data['email']
	firstName 	= f.cleaned_data['firstName']
	middleName 	= f.cleaned_data['middleName']
	lastName 	= f.cleaned_data['lastName']
	dob 		= f.cleaned_data['dob']

	dobObject = 0
	if models.DateOfBirth.objects.filter(dob = dob).count() != 1:
		dobObject = models.DateOfBirth.objects.create(dob = dob, age = 2016 - f.getYear())

	else:
		dobObject = models.DateOfBirth.objects.get(dob = dob)

	newuser = models.MyUser.objects.create(username = username, email = email, first_name = firstName, middle_name = middleName, last_name = lastName, is_active = False, dob = dobObject)
	newuser.set_password(password)
	newuser.save()

	otp = models.createOTP(newuser, 'AA')
	targetUser = newuser
	recipient_email = email
	sender = settings.EMAIL_HOST_USER
	subject = 'Just one step away from accessing our services.'
	link = 'localhost:8000/account/confirm/' + str(newuser.userID) + '/' + str(otp)
	content = loader.render_to_string('account/sentMail-aa.html', {'link' : link})

	message = EmailMultiAlternatives(subject, content, sender, [recipient_email])
	message.send()

	string = "An email has been sent to you on '" + recipient_email + "' for confirmation. Follow the link received to activate your account."
	return HttpResponse(render(request, 'common/success_NotLoggedIn.html', {'message' : string}))


@require_http_methods(['GET', 'POST'])
def logout(request):
	auth_logout(request)
	return redirect(reverse('login'))
