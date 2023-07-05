from django.db.models.signals import post_save
from .models import User, Profile, Student


def create_profile(sender, instance:User, created, **kwargs):
    if created:
        user = instance
        profile = Profile.objects.create(
            user=user,
            name=user.full_name
        )
        profile.save()

def create_student_post_save_handeler(sender, instance:User, created ,*args ,**kwargs):
    if created:
        student = Student.objects.create(user=instance)
        student.save()


post_save.connect(create_profile, sender=User)
post_save.connect(create_student_post_save_handeler, sender=User)
