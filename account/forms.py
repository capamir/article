from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth.forms import UserCreationForm as BaseUserCreationForm
from .models import User, OtpCode, Profile, Message


class UserCreationForm(forms.ModelForm):
	password1 = forms.CharField(label='password', widget=forms.PasswordInput)
	password2 = forms.CharField(label='confirm password', widget=forms.PasswordInput)

	class Meta:
		model = User
		fields = ('full_name', 'email', 'phone_number')
		labels = {'full_name': 'Name', 'phone_number': 'Phone Number'}

	def clean_password2(self):
		cd = self.cleaned_data
		if cd['password1'] and cd['password2'] and cd['password1'] != cd['password2']:
			raise ValidationError('passwords dont match')
		return cd['password2']
	
	def clean_email(self):
		email = self.cleaned_data['email']
		user = User.objects.filter(email=email).exists()
		if user:
			raise ValidationError('This email already exists')
		return email

	def clean_phone_number(self):
		phone_number = self.cleaned_data['phone_number']
		user = User.objects.filter(phone_number=phone_number).exists()
		if user:
			raise ValidationError('This phone_number already exists')
		return phone_number


	def save(self, commit=True):
		user = super().save(commit=False)
		user.set_password(self.cleaned_data['password1'])
		if commit:
			user.save()
		return user


class UserChangeForm(forms.ModelForm):
	password = ReadOnlyPasswordHashField(help_text="you can change password using <a href=\"../password/\">this form</a>.")

	class Meta:
		model = User
		fields = ('full_name', 'email', 'phone_number', 'password', 'last_login', 'role')
		labels = {'full_name': 'Name', 'phone_number': 'Phone Number'}


class UserRegistrationForm(BaseUserCreationForm):
	class Meta:
		model = User
		fields = ('full_name', 'email', 'phone_number', 'password1', 'password2')
		labels = {'full_name': 'Name', 'phone_number': 'Phone Number',}

	def __init__(self, *args, **kwargs):
		super(UserRegistrationForm, self).__init__(*args, **kwargs)

		for name, field in self.fields.items():
			field.widget.attrs.update({'class': 'input'})

	def clean_email(self):
		email = self.cleaned_data['email']
		user = User.objects.filter(email=email).exists()
		if user:
			raise ValidationError('This email already exists')
		return email

	def clean_phone(self):
		phone = self.cleaned_data['phone_number']
		user = User.objects.filter(phone_number=phone).exists()
		if user:
			raise ValidationError('This phone number already exists')
		OtpCode.objects.filter(phone_number=phone).delete()
		return phone


class VerifyCodeForm(forms.Form):
	code = forms.IntegerField(widget=forms.TextInput(attrs={"class": "input"}))


class UserLoginForm(forms.Form):
	phone = forms.CharField(widget=forms.TextInput(attrs={"class": "input form-control"}))
	password = forms.CharField(widget=forms.PasswordInput(attrs={"class": "input form-control"}))


class ProfileForm(forms.ModelForm):
	class Meta:
		model = Profile
		fields = ('location', 'bio', 'short_intro', 'image',
				  'social_github', 'social_linkedin', 'social_twitter',
				  'social_website')
	
	# def __init__(self, *args, **kwargs):
	# 	for name, field in self.fields.items():
	# 		field.widget.attrs.update({'class': 'input'})


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['name', 'email', 'subject', 'body']