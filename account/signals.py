from django.db.models.signals import post_save
from .models import User, Profile


def create_profile(sender, instance:User, created, **kwargs):
    if created:
        user = instance
        profile = Profile.objects.create(
            user=user,
            name=user.full_name
        )
        profile.save()


post_save.connect(create_profile, sender=User)
