from django import forms
from .import models


class SendMailForm(forms.Form):
	to 		= forms.CharField(max_length = 35)
	subject = forms.CharField(max_length = 35)
	body 	= forms.CharField(max_length = 500)
	attachment = forms.ImageField(required = False)


class ImageForm(forms.Form):
	address = forms.ImageField()
