from django.db import models
from account.models import User

# Create your models here.
class ArticleModel(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField(max_length=500)
    file = models.FileField(upload_to='articles')