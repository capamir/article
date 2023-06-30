from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.urls import reverse
import uuid
from .managers import UserManager


# Create your models here.
class User(AbstractBaseUser, PermissionsMixin):
	ROLE_TYPE = (
		('student', 'student'),
		('proffesor', 'proffesor'),
		('manager', 'manager'),
	)
	role = models.CharField(max_length=200, choices=ROLE_TYPE, blank=True, null=True)
	email = models.EmailField(max_length=255, unique=True)
	phone_number = models.CharField(max_length=11, unique=True)
	full_name = models.CharField(max_length=100)
	is_active = models.BooleanField(default=True)
	is_admin = models.BooleanField(default=False)
	
	id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)    


	objects = UserManager()

	USERNAME_FIELD = 'phone_number'
	REQUIRED_FIELDS = ['email', 'full_name']

	def __str__(self):
		return self.email

	@property
	def is_staff(self):
		return self.is_admin
	
	def get_absolute_url(self):
		return reverse('account:profile_detail', args=[self.id,])


class Professor(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	
	def __str__(self):
		return self.user

class OtpCode(models.Model):
	phone_number = models.CharField(max_length=11, unique=True)
	code = models.PositiveSmallIntegerField()
	created = models.DateTimeField(auto_now=True)

	def __str__(self):
		return f'{self.phone_number} - {self.code} - {self.created}'