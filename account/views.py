from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.views import View
import random

from .models import User, OtpCode
from .forms import UserRegistrationForm, VerifyCodeForm, UserLoginForm
from utils import send_otp_code

#email_modules
from django.core.mail import EmailMessage
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string

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
			send_otp_code(cd['phone_number'], random_code)
			OtpCode.objects.create(phone_number=cd['phone_number'], code=random_code)
			
			request.session['user_registration_info'] = {
				'phone_number': cd['phone_number'],
				'email': cd['email'],
				'full_name': cd['full_name'],
				'password': cd['password1'],
			}
   
			#send_email
			to_email= cd['email']
			mail_subject = 'حساب کاربری رو فعال کن!'
			message = render_to_string('account/active_email/email_activation.html', {
				'full_name': f"{cd['full_name']}",
				'domain': get_current_site(request).domain,
				'activation_code': random_code,
				'protocol': 'https' if request.is_secure() else 'http'
			})
			email = EmailMessage(mail_subject, message, to=[to_email])
			email.content_subtype = 'html'
			if email.send():
				request.session["register_msg"] = True
			else:
				request.session["failed_register_msg"] = True
   
			messages.success(request, 'we sent you a code', 'success')
			return redirect('account:verify_code')
		return render(request, self.template_name, {'form':form})


class UserRegisterVerifyCodeView(View):
	form_class = VerifyCodeForm

	def get(self, request):
		context = {'form':self.form_class}
		return render(request, 'account/auth/verify_code.html', context)

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


class UserLoginView(View):
	form_class = UserLoginForm
	template_name = 'account/auth/login.html'

	def dispatch(self, request, *args, **kwargs):
		if request.user.is_authenticated:
			return redirect('articles:articles')
		return super().dispatch(request, *args, **kwargs)

	def get(self, request):
		context = {'form': self.form_class}
		return render(request, self.template_name, context)

	def post(self, request):
		form = self.form_class(request.POST)
		if form.is_valid():
			cd = form.cleaned_data
			user = authenticate(request, phone_number=cd['phone'], password=cd['password'])
			if user is not None:
				login(request, user)
				messages.success(request, 'you logged in successfully', 'info')
				return redirect('articles:articles')
			messages.error(request, 'phone or password is wrong', 'warning')
		return render(request, self.template_name, {'form':form})
	