from django.db import models
from account.models import User

# Create your models here.
class ArticleModel(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField(max_length=500)
    file = models.FileField(upload_to='articles')

class ReviewModel(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    article = models.ForeignKey(ArticleModel, on_delete=models.CASCADE)
    body = models.TextField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)