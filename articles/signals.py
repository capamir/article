# ===== signals ===== 
from django.dispatch import receiver
from django.db.models.signals import post_save,pre_save,m2m_changed
from django.db import transaction
from account.models import User, Professor

from .models import Article,Review

@receiver(pre_save, sender=Article)
def article_pre_save_handler(sender, instance:Article, *args, **kwargs):
    # print("pre",instance.judges.all())
    pass
    
@receiver(post_save, sender=Article)
def article_post_save_handler(sender, instance:Article, created, *args, **kwargs):
    if created:
        pass
    else:
        pass
        
@receiver(m2m_changed, sender=Article.judges.through)
def articel_update_when_judge_added(sender, instance:Article, action, *args, **kwargs):
    if action == "post_add":
        # create review rows for judge if m2m changed
        get_judge_list = instance.judges.all()
        if get_judge_list:
            with transaction.atomic():
                for judge in get_judge_list:
                    judge:Professor = judge 
                    get,c = Review.objects.get_or_create(owner=judge, article=instance)
                    if(c):
                        get.save()
