# ===== signals ===== 
from django.dispatch import receiver
from django.db.models.signals import post_save,pre_save,m2m_changed,post_delete
from django.db import transaction
from account.models import User, Professor
from datetime import datetime

from .models import Article,Review


def article_pre_save_handeler(sender, instance:Article, *args, **kwargs):
    instance.admin_last_view = datetime.now()
        
@receiver(m2m_changed, sender=Article.judges.through)
def articel_update_when_judge_added(sender, instance:Article, action, *args, **kwargs):
    if action == "post_add":
        # create review rows for judge if m2m changed
        get_judge_list = instance.judges.all()
        if get_judge_list:
            with transaction.atomic():
                for judge in get_judge_list:
                    judge:Professor = judge 
                    get,create = Review.objects.get_or_create(owner=judge, article=instance)
                    if(create):
                        get.save()
                        

def review_post_save_handler(sender, instance:Review, created, *args, **kwargs):
    if created:
        find_article = instance.article
        find_article.is_view = True
        find_article.save()
            
        
def review_post_delete_handeler(sender, instance:Review, *args, **kwargs):
    find_article = instance.article
    find_judge = instance.owner
    find_article.judges.remove(find_judge)
    if(find_article.judges.exists() == False):
        find_article.is_view = False
    # save article with out send signal,
    Article.objects.bulk_update([find_article,],fields=["is_view"])


post_save.connect(review_post_save_handler, sender=Review)
post_delete.connect(review_post_delete_handeler, sender=Review)
pre_save.connect(article_pre_save_handeler, sender=Article)
