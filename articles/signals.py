# from django.dispatch import receiver
# from django.db.models.signals import post_save

# from .models import Article,Review,Notification_Manager

# @receiver(post_save, sender=Article)
# def article_post_save_handler(sender, instance:Article, created, *args, **kwargs):
#     if created:
#         # create notification that new article added
#         new_notife = Notification_Manager.objects.create(article=sender)
#         new_notife.save()
#     else:
#         # create review rows for judge
#         pass
#         # get_judge_list = instance.judges.all()
#         # get_user = instance.owner
#         # li = []
        
#         # for judge in get_judge_list:
#         #     pass