from django.db.models.signals import post_save
from .models import User, Profile


def create_profile(sender, instance, created, **kwargs):
    if created:
        user = instance
        profile = Profile.objects.create(
            user=user,
        )
        profile.save()


# def update_user(sender, instance:Profile, created, **kwargs):
#     if not created:
#         profile = instance
#         user = profile.user
#         user.first_name = profile.name
#         user.email = profile.email
#         user.username = profile.username
#         user.save()



post_save.connect(create_profile, sender=User)
# post_save.connect(update_user, sender=Profile)
