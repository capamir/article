from django.db import models
from account.models import User, Professor
import uuid


# Create your models here.
class Article(models.Model):
    owner = models.ForeignKey(User,on_delete=models.CASCADE)
    judges = models.ManyToManyField(Professor, related_name='articles',default=None,blank=True)
    title = models.CharField(max_length=200)
    description = models.TextField(max_length=500)
    file = models.FileField(upload_to='articles')
    created = models.DateTimeField(auto_now_add=True)

    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)     
    
    def __str__(self):
        return self.title

class Review(models.Model):
    owner = models.ForeignKey(Professor, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    body = models.TextField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False) 
    
    def __str__(self):
        return f"{self.owner} - {self.article.title}"