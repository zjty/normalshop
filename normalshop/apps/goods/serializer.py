# _*_ coding:utf-8 _*_
__author__ = 'zjty'
__date__ = '2018/4/25 上午9:43'

from django.db.models import Q
from rest_framework import serializers

from .models import Goods, GoodsCategory, HotSearchWords, GoodsImage, Banner
from goods.models import GoodsCategoryBrand, IndexAd


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


class HotWordsSerializer(serializers.ModelSerializer):

    class Meta:
        model = HotSearchWords
        fields = "__all__"


class BannerSerializer(serializers.ModelSerializer):
    goods = GoodsSerializer(many=False)

    class Meta:
        model = Banner
        fields = "__all__"


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = GoodsCategoryBrand
        fields = "__all__"


class IndexCategorySerializer2(serializers.ModelSerializer):

    class Meta:
        model = GoodsCategory
        fields = ("name", "id")


class IndexCategorySerializer(serializers.ModelSerializer):
    brands = BrandSerializer(many=True)
    sub_cat = IndexCategorySerializer2(many=True)
    goods = serializers.SerializerMethodField()
    ad_goods = serializers.SerializerMethodField()

    def get_goods(self, obj):
        all_goods = Goods.objects.filter(Q(category_id=obj.id) | Q(category__parent_category_id=obj.id)
                                         | Q(category__parent_category__parent_category_id=obj.id))
        goods_serializer = GoodsSerializer(all_goods, many=True, context={'request': self.context['request']})
        return goods_serializer.data

    def get_ad_goods(self, obj):
        goods_json = {}
        ad_goods = IndexAd.objects.filter(category_id=obj.id, )
        if ad_goods:
            good_ins = ad_goods[0].goods
            goods_json = GoodsSerializer(good_ins, many=False, context={'request': self.context['request']}).data
        return goods_json

    class Meta:
        model = GoodsCategory
        fields = "__all__"
