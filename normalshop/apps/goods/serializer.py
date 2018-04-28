# _*_ coding:utf-8 _*_
__author__ = 'zjty'
__date__ = '2018/4/25 上午9:43'


from rest_framework import serializers

from .models import Goods, GoodsCategory, HotSearchWords, GoodsImage, Banner
from goods.models import GoodsCategoryBrand, IndexAd


class GoodsCategoryBrandSerializer(serializers.ModelSerializer):

    class Meta:
        model = GoodsCategoryBrand
        fields = "__all__"


class CategorySerializer3(serializers.ModelSerializer):

    class Meta:
        model = GoodsCategory
        fields = "__all__"


class CategorySerializer2(serializers.ModelSerializer):
    sub_cat = CategorySerializer3(many=True)

    class Meta:
        model = GoodsCategory
        fields = "__all__"


class CategorySerializer(serializers.ModelSerializer):
    sub_cat = CategorySerializer2(many=True)
    # brands = GoodsCategoryBrandSerializer()

    class Meta:
        model = GoodsCategory
        fields = "__all__"


class GoodsImageSerilizer(serializers.ModelSerializer):

    class Meta:
        model = GoodsImage
        fields = ("image",)


class GoodsSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    images = GoodsImageSerilizer(many=True)

    class Meta:
        model = Goods
        fields = "__all__"


class HotSearchWordsSerializer(serializers.ModelSerializer):

    class Meta:
        model = HotSearchWords
        fields = "__all__"

