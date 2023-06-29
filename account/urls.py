from django.urls import path, include
from . import views

password = [
    path('reset/', views.UserPasswordResetView.as_view(), name='reset_password'),
	path('reset/done/', views.UserPasswordResetDoneView.as_view(), name='password_reset_done'),
	path('confirm/<uidb64>/<token>/', views.UserPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
	path('confirm/complete', views.UserPasswordResetCompleteView.as_view(), name='password_reset_complete'),
]


app_name = 'account'
urlpatterns = [
    path('', views.ProfilesView.as_view(), name='profiles'),
    path('profile', views.UserAccountView.as_view(), name='account'),

    path('register/', views.UserRegistrationView.as_view(), name='register'),
    path('verify/', views.UserRegisterVerifyCodeView.as_view(), name='verify_code'),
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('logout/', views.UserLogoutView.as_view(), name='logout'),
    
    path('password/', include(password)),

    path('<str:pk>/', views.ProfileDetailView.as_view(), name='profile_detail'),

]

