from django.dispatch import receiver
from django.db.models.signals import post_save

from .models import Article,Review

@receiver(post_save, sender=Article)
def article_created_handler(sender, instance, created, *args, **kwargs):
    if created:
        # created review row for judges in article
        pass
    else:
        pass