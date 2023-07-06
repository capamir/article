from django.db.models.signals import post_save
from .models import User, Profile, Student, Professor


def create_profile(sender, instance: User, created, **kwargs):
    if created:
        user = instance
        profile = Profile.objects.create(
            user=user,
            name=user.full_name
        )
        profile.save()


def create_student_post_save_handeler(sender, instance: User, created, *args, **kwargs):
    if created:
        student = Student.objects.create(user=instance)
        student.save()


def remove_student(sender, instance: Professor, created, **kwargs):
    # removes student role when a user becomes Professor
    if created:
        try:
            student = instance.user.student
            student.delete()
        except:
            pass


post_save.connect(create_profile, sender=User)
post_save.connect(create_student_post_save_handeler, sender=User)
post_save.connect(remove_student, sender=Professor)
