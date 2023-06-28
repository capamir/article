from django.shortcuts import render, redirect
from django.contrib import messages
from django.views import View
import random

from .models import User, OtpCode
from .forms import UserRegistrationForm, VerifyCodeForm
from utils import send_otp_code

# Create your views here.
class UserRegistrationView(View):
	form_class = UserRegistrationForm
	template_name = 'account/auth/register.html'

	def get(self, request):
		context = {'form': self.form_class}
		return render(request, self.template_name, context)

	def post(self, request):
		form = self.form_class(request.POST)
		if form.is_valid():
			cd = form.cleaned_data
			random_code = random.randint(1000, 9999)
			send_otp_code(cd['phone'], random_code)
			OtpCode.objects.create(phone_number=cd['phone_number'], code=random_code)
			
			request.session['user_registration_info'] = {
				'phone_number': cd['phone_number'],
				'email': cd['email'],
				'full_name': cd['full_name'],
				'password': cd['password'],
			}
			messages.success(request, 'we sent you a code', 'success')
			return redirect('account:verify_code')
		return render(request, self.template_name, {'form':form})


class UserRegisterVerifyCodeView(View):
	form_class = VerifyCodeForm

	def get(self, request):
		context = {'form':self.form}
		return render(request, 'account/verify.html', context)

	def post(self, request):
		user_session = request.session['user_registration_info']
		code_instance = OtpCode.objects.get(phone_number=user_session['phone_number'])
		form = self.form_class(request.POST)
		if form.is_valid():
			cd = form.cleaned_data
			if cd['code'] == code_instance.code:
				User.objects.create_user( user_session['phone_number'], user_session['email'],
										 user_session['full_name'], user_session['password'])

				code_instance.delete()
				messages.success(request, 'you registered.', 'success')
				return redirect('articles:articles')
			else:
				messages.error(request, 'this code is wrong', 'danger')
				return redirect('account:verify_code')
		return redirect('articles:articles')
