# ===== signals =====
from django.dispatch import receiver
from django.db.models.signals import post_save, pre_save, m2m_changed, post_delete
from django.db import transaction
from account.models import User, Professor
from datetime import datetime

from .models import Article, Review
from account.models import Message


def article_pre_save_handeler(sender, instance: Article, *args, **kwargs):
    instance.admin_last_view = datetime.now()

# todo: signal for update article to send notification message


# @receiver(m2m_changed, sender=Article.judges.through)
# def articel_update_when_judge_added(sender, instance:Article, action, *args, **kwargs):
#     if action == "post_add":
#         # create review rows for judge if m2m changed
#         get_judge_list = instance.judges.all()
#         if get_judge_list:
#             with transaction.atomic():
#                 for judge in get_judge_list:
#                     judge:Professor = judge
#                     get,create = Review.objects.get_or_create(owner=judge, article=instance)
#                     if(create):
#                         get.save()

@receiver(m2m_changed, sender=Article.judges.through)
def articel_update_when_judge_added(sender, instance: Article, action, pk_set, *args, **kwargs):
    with transaction.atomic():
        student = instance.owner
        if action == "post_add":
            for pk in pk_set:
                professor = Professor.objects.get(pk=pk)
                review = Review.objects.create(
                    owner=professor, article=instance)
                message_professor = Message.objects.create(
                    recipient=professor.user,
                    name="admin",
                    subject=f"You have {instance.title} article to judge",
                    body=f"greetings professor {professor.user.full_name}\n you need to review an article that we added to your user panel."
                )
                message_student = Message.objects.create(
                    recipient=student,
                    name="admin",
                    subject=f"{professor.user.full_name} will see your article: {instance.title}",
                    body=f"greetings dear {student.full_name}\n Professor {professor.user.full_name} will review your {instance.title} article. \n You can check the reviews in your user panel."
                )

        elif action == "post_remove":
            for pk in pk_set:
                professor = Professor.objects.get(pk=pk)
                review = Review.objects.filter(owner=professor)
                if review.exists:
                    review.delete()
                message_professor = Message.objects.create(
                    recipient=professor.user,
                    name="admin",
                    subject="You removed from judging an article",
                    body=f"greetings professor {professor.user.full_name}\n your access to review {instance.title} article from {student.full_name} is no longer exist."
                )
                message_student = Message.objects.create(
                    recipient=student,
                    name="admin",
                    subject=f"{professor.user.full_name} removed from judging your article: {instance.title}",
                    body=f"greetings dear {student.full_name}\n Professor {professor.user.full_name} will no longer review your {instance.title} article. \n You can check the reminding reviews in your user panel."
                )


def review_post_save_handler(sender, instance: Review, created, *args, **kwargs):
    if created:
        find_article = instance.article
        find_article.is_view = True
        find_article.save()


def review_post_delete_handeler(sender, instance: Review, *args, **kwargs):
    find_article = instance.article
    find_judge = instance.owner
    find_article.judges.remove(find_judge)
    if (find_article.judges.exists() == False):
        find_article.is_view = False
    # save article with out send signal,
    Article.objects.bulk_update([find_article,], fields=["is_view"])


post_save.connect(review_post_save_handler, sender=Review)
post_delete.connect(review_post_delete_handeler, sender=Review)
pre_save.connect(article_pre_save_handeler, sender=Article)
