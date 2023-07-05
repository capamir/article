from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin,PermissionRequiredMixin
from django.contrib.auth.views import LogoutView
from django.contrib.auth import views as auth_views
from django.views import View
from django.views.generic import ListView, DetailView
from django.urls import reverse_lazy,reverse
import random

from .models import User, OtpCode, Profile
from .forms import UserRegistrationForm, VerifyCodeForm, UserLoginForm, ProfileForm, MessageForm
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
				return redirect('account:account')
			messages.error(request, 'phone or password is wrong', 'warning')
		return render(request, self.template_name, {'form':form})


class UserLogoutView(LoginRequiredMixin, LogoutView):
	next_page = '/'

# ---------------------- reset password ------------------------
class UserPasswordResetView(auth_views.PasswordResetView):
	template_name = 'account/password/password_reset_form.html'
	success_url = reverse_lazy('account:password_reset_done')
	email_template_name = 'account/password/password_reset_email.html'


class UserPasswordResetDoneView(auth_views.PasswordResetDoneView):
	template_name = 'account/password/password_reset_done.html'


class UserPasswordResetConfirmView(auth_views.PasswordResetConfirmView):
	template_name = 'account/password/password_reset_confirm.html'
	success_url = reverse_lazy('account:password_reset_complete')


class UserPasswordResetCompleteView(auth_views.PasswordResetCompleteView):
	template_name = 'account/password/password_reset_complete.html'
# ---------------------- End reset password ------------------------


# ---------------------- Profile ------------------------

            	

class ProfilesView(PermissionRequiredMixin, LoginRequiredMixin, ListView):
	template_name = 'account/profile/profiles.html'
	model = Profile
	context_object_name = 'profiles'
	permission_required = 'profile.view_profile'
 

class ProfileDetailView(PermissionRequiredMixin, LoginRequiredMixin, DetailView):
	template_name = 'account/profile/profile_detail.html'
	model = Profile
	context_object_name = 'profile'
	permission_required = 'profile.view_profile'
 
 
	def dispatch(self, request, *args, **kwargs):
		if request.user.id == kwargs['pk']:
			return redirect('account:account')
		return super().dispatch(request, *args, **kwargs)
	

class UserAccountView(LoginRequiredMixin, View):
	template_name = 'account/profile/account.html'
	def get(self, request, *args, **kwargs):
		context = {'profile': request.user.profile, 'student': request.user.student_set.all(), 'professor': request.user.professor_set.all()}
		return render(request, self.template_name, context)
	
class UpdateUserProfileView(LoginRequiredMixin, View):
    template_name = 'account/profile/profile_form.html'
    form_class = ProfileForm

    def setup(self, request, *args, **kwargs):
        self.profile = request.user.profile
        return super().setup(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        form = self.form_class(instance=self.profile)
        context = {'form': form}
        return render(request, self.template_name, context=context)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            cd = form.cleaned_data
            find_user_profile_obj = Profile.objects.get(user=request.user.id)
            find_user_profile_obj.location = cd["location"]
            find_user_profile_obj.bio = cd["bio"]
            find_user_profile_obj.short_intro = cd["short_intro"]
            find_user_profile_obj.social_github = cd["social_github"]
            find_user_profile_obj.social_linkedin = cd["social_linkedin"]
            find_user_profile_obj.social_twitter = cd["social_twitter"]
            find_user_profile_obj.social_website = cd["social_website"]
            find_user_profile_obj.save()
            # form.save()
            return redirect('account:account')
        context = {'form': form, 'user': request.user.profile}
        return render(request, self.template_name, context=context)

# ---------------------- End Profile ------------------------

# ----------------------  Message ------------------------
class InboxView(LoginRequiredMixin, View):
    template_name = 'account/message/inbox.html'

    def get(self, request, *args, **kwargs):
        profile = request.user.profile
        message_requests = profile.messages.all()
        unread_count = message_requests.filter(is_read=False).count()
        context = {
            'message_requests': message_requests,
            'unread_count': unread_count
        }
        return render(request, self.template_name, context)


class MessageView(LoginRequiredMixin, View):
    template_name = 'account/message/message.html'

    def get(self, request, *args, **kwargs):
        profile = request.user.profile
        message = profile.messages.get(id=kwargs['pk'])
        if message.is_read == False:
            message.is_read = True
            message.save()

        context = {'message': message}
        return render(request, self.template_name, context)


class CreateMessageView(LoginRequiredMixin, View):
    template_name = 'account/message/message_form.html'
    form_class = MessageForm

    def setup(self, request, *args, **kwargs):
        try:
            self.sender = request.user.profile
        except:
            self.sender = None
        self.recipient = Profile.objects.get(id=kwargs['pk'])
        return super().setup(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):

        context = {
            'form': self.form_class,
            'recipient': self.recipient
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = self.sender
            message.recipient = self.recipient
            if self.sender:
                message.name = self.sender.name
                message.email = self.sender.email
            message.save()
            messages.success(request, 'Your message was successfully sent!')
            return redirect('account:profile-detail', pk=self.recipient.id)

        context = {
            'form': form,
            'recipient': self.recipient
        }
        return render(request, self.template_name, context)

# ----------------------  End Message ------------------------
