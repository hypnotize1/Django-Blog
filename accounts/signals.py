from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Profile


@receiver(post_save, sender=User)
def handle_user_profile(sender, instance, created, **kwargs):
    """Ensures every user has a profile"""
    Profile.objects.get_or_create(user=instance)