from django.urls import path, include
from . import views


app_name = 'account'
urlpatterns = [
    path('register/', views.UserRegistrationView.as_view(), name='register'),
    path('verify/', views.UserRegisterVerifyCodeView.as_view(), name='verify_code'),
    path('login/', views.UserLoginView.as_view(), name='login'),
    
]

