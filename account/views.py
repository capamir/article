from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.generic import CreateView

from .forms import UserRegistrationForm 

# Create your views here.
class UserRegistrationView(CreateView):
    form_class = UserRegistrationForm
    template_name = 'accounts/auth/register.html'
    success_url = '/'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('articles:articles')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        messages.success(
            self.request, 'you registered successfully', 'success')
        return super().form_valid(form)
