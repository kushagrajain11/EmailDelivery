from django.db import models
from random import randint
from django.contrib.auth.models import AbstractUser
from mail import models as MailModels


class DateOfBirth(models.Model):
	dob = models.DateField(primary_key = True)
	age = models.IntegerField()


class MyUser(AbstractUser):
	userID 				= models.AutoField(primary_key = True)
	middle_name			= models.CharField(max_length = 35)
	dob 				= models.ForeignKey(DateOfBirth)
	receivedMessages 		= models.ManyToManyField(MailModels.Message, related_name = 'received_by')


class OTP(models.Model):
	code 		= models.IntegerField(primary_key = True)
	dateTime 	= models.DateTimeField(auto_now_add = True)
	user 		= models.ForeignKey(MyUser)
	purpose 	= models.CharField(max_length = 2)


def createOTP(user, purpose):
	if purpose != 'FP' and purpose != 'AA':
		return

	existing = OTP.objects.filter(user = user)

	if existing.count() > 0:
		for item in existing:
			item.delete()

	code = randint(100000, 999999)

	while(OTP.objects.filter(code = code).count() > 0):
		code = randint(100000, 999999)

	OTPObject = OTP.objects.create(code = code, user = user, purpose = purpose)
	OTPObject.save()
	return code
