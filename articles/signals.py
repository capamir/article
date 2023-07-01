# ===== signals ===== 
from django.dispatch import receiver
from django.db.models.signals import post_save,pre_save
from django.db import transaction
from account.models import User, Professor

from .models import Article,Review,Notification_Manager

@receiver(pre_save, sender=Article)
def article_pre_save_handler(sender, instance:Article, *args, **kwargs):
    print("pre",instance.judges.all())

@receiver(post_save, sender=Article)
def article_post_save_handler(sender, instance:Article, created, *args, **kwargs):
    if created:
        # create notification that new article added
        new_notife = Notification_Manager.objects.create(article=instance)
        new_notife.save()
    else:
        # create review rows for judge
        print("post",instance.judges.all())
        # if get_judge_list:
        #     with transaction.atomic():
        #         for judge in get_judge_list:
        #             judge:Professor = judge 
        #             get,c = Review.objects.get_or_create(owner=judge, article=instance)
        #             if(c):
        #                 get.save()