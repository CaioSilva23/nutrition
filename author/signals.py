from .models import Profile
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User


@receiver(post_save, sender=User)
def cria_profile(sender, instance, created, **kwargs):
    if created:
        profile = Profile(author=instance)
        profile.save()
