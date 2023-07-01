from django.db import models
from account.models import User, Professor
import uuid
from django.db import transaction

# Create your models here.
class Article(models.Model):
    owner = models.ForeignKey(User,on_delete=models.CASCADE)
    judges = models.ManyToManyField(Professor, related_name='articles', null=True, default=None, blank=True)
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
    
class Notification_Manager(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
     
    def __str__(self):
        return self.article.title
    
# ===== signals ===== 
from django.dispatch import receiver
from django.db.models.signals import post_save,pre_save

from .models import Article,Review,Notification_Manager

@receiver(pre_save, sender=Article)
def article_post_save_handler(sender, instance:Article, *args, **kwargs):
    pass

@receiver(post_save, sender=Article)
def article_post_save_handler(sender, instance:Article, created, *args, **kwargs):
    if created:
        # create notification that new article added
        new_notife = Notification_Manager.objects.create(article=instance)
        new_notife.save()
    else:
        # create review rows for judge
        get_judge_list = instance.judges.all()
        if get_judge_list is not None:
            with transaction.atomic():
                for judge in get_judge_list:
                    judge:Professor = judge 
                    get,c = Review.objects.get_or_create(owner=judge, article=instance)
                    if(c):
                        get.save()    
        else:
            pass