# _*_ coding:utf-8 _*_
__author__ = 'zjty'
__date__ = '2018/4/29 下午4:25'
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from user_operation.models import UserFav


@receiver(post_save, sender=UserFav)
def create_userfav(sender, instance=None, created=False, **kwargs):
    if created:
        goods = instance.goods
        goods.fav_num += 1
        goods.save()


@receiver(post_delete, sender=UserFav)
def delete_userfav(sender, instance=None, created=False, **kwargs):
    goods = instance.goods
    goods.fav_num -= 1
    goods.save()
