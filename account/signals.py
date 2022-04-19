from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

from .models import Account


@receiver(post_save, sender=Account)
def create_auth_token(sender, instance, created, **kwargs):
    if created:
        token = Token.objects.create(user=instance.user)
        instance.token = token.key
        instance.save()

