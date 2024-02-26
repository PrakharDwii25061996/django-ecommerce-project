from django.db.models.signals import post_save, pre_delete
from django.contrib.auth.models import User
from django.dispatch import receiver

from .models import CustomUser
from apps.cart.models import Cart
from apps.user.models import Profile


@receiver(post_save, sender=CustomUser) 
def create_profile(sender, instance, created, **kwargs):
    if created:
        Cart.objects.create(user=instance)

        Profile.objects.create(user=instance)
