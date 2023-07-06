from django.db import models
from account.models import User, Professor
import uuid
from django.core.validators import FileExtensionValidator
from ckeditor.fields import RichTextField
from django.core.validators import MaxValueValidator, MinValueValidator
# Create your models here.


class Article(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    judges = models.ManyToManyField(
        Professor, related_name='articles', default=None, blank=True)
    title = models.CharField(max_length=200)
    description = RichTextField()
    file = models.FileField(upload_to='articles', validators=[
                            FileExtensionValidator(['pdf'])])
    is_view = models.BooleanField(default=False)
    admin_last_view = models.DateTimeField(
        auto_created=False, default=None, null=True)
    updated = models.DateTimeField(auto_now_add=True)

    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)

    def __str__(self):
        return self.title

# todo : add score field to review model


class Review(models.Model):
    owner = models.ForeignKey(Professor, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    body = RichTextField(default='',)
    score = models.PositiveSmallIntegerField(default=0, validators=[
        MaxValueValidator(100),
        MinValueValidator(0)
    ])
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)

    def __str__(self):
        return f"{self.owner} - {self.article.title}"
