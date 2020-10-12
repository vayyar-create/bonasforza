from django import forms
from django.core.exceptions import ValidationError
from PIL import Image

from .models import *


class LoginForm(forms.Form):
	username=forms.CharField(max_length=75)
	password=forms.CharField(max_length=32, widget=forms.PasswordInput)

	username.widget.attrs.update({'class': 'single-input-primary'})
	password.widget.attrs.update({'class': 'single-input-primary'})




class MailForm(forms.Form):
	name=forms.CharField(max_length=100)
	email=forms.EmailField(max_length=254)
	subject=forms.CharField(max_length=254, required=True)
	message = forms.CharField(max_length=3000, widget=forms.Textarea, required=True)

	name.widget.attrs.update({'class': 'form-control', 'placeholder': 'Enter your name'})
	email.widget.attrs.update({'class': 'form-control', 'placeholder': 'Enter email address'})
	subject.widget.attrs.update({'class': 'form-control', 'placeholder': 'Enter Subject'})
	message.widget.attrs.update({'class': 'form-control', 'placeholder': 'Enter Message', 'rows' : 1})




class DogForm(forms.ModelForm):

	class Meta:
		model=Dog
		fields=['name', 'born_date', 'parents', 'breeder_or_kennel', 'titles', 'working_titles', 'tests', 'facebook', 'main_image']

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields['breeder_or_kennel'].required = False
		self.fields['titles'].required = False
		self.fields['working_titles'].required = False
		self.fields['tests'].required = False
		self.fields['facebook'].required = False

		for field in self.fields.values():
			field.widget.attrs['class'] = 'single-input-primary'
			field.widget.attrs['type'] = 'text'
		self.fields['parents'].widget.attrs['class'] = 'single-textarea'
		self.fields['parents'].widget.attrs['rows'] = 4

		self.fields['titles'].widget.attrs['class'] = 'single-textarea'
		self.fields['titles'].widget.attrs['rows'] = 5

		self.fields['working_titles'].widget.attrs['class'] = 'single-textarea'
		self.fields['working_titles'].widget.attrs['rows'] = 4

		self.fields['tests'].widget.attrs['class'] = 'single-textarea'
		self.fields['tests'].widget.attrs['rows'] = 3

						
					


