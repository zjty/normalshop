# _*_ coding:utf-8 _*_
__author__ = 'zjty'
__date__ = '2018/4/25 下午5:14'
from django.db.models import Q

from django_filters import rest_framework as filters

from .models import Goods


class GoodsFilter(filters.FilterSet):
    pricemin = filters.NumberFilter(name="shop_price", lookup_expr='gte')
    pricemax = filters.NumberFilter(name="shop_price", lookup_expr='lte')
    top_category = filters.NumberFilter(method='top_category_filter')

    def top_category_filter(self, queryset, name, value):
        queryset = queryset.filter(Q(category_id=value) | Q(category__parent_category_id=value) \
                                   | Q(category__parent_category__parent_category_id=value))
        return queryset

    class Meta:
        model = Goods
        fields = ['pricemin', 'pricemax']

