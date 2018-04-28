# _*_ coding:utf-8 _*_
__author__ = 'zjty'
__date__ = '2018/4/27 上午10:39'
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model

User = get_user_model()


@receiver(post_save, sender=User)
def encryption_password(sender, instance=None, created=False, **kwargs):
    if created:
        password = instance.password
        instance.set_password(password)
        instance.save()
        # Token.objects.create(user=instance)