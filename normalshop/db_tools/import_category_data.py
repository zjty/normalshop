# _*_ coding:utf-8 _*_
__author__ = 'zjty'
__date__ = '2018/4/24 下午3:54'

import os
import sys


pwd = os.path.dirname(os.path.abspath(__file__))
sys.path.append(pwd+'../')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "normalshop.settings")

import django
django.setup()


from goods.models import GoodsCategory

from db_tools.data.category_data import row_data


def deal_category(data, depth, category_pro):
    if not isinstance(data, (list, dict)):
        raise TypeError("数据格式不正确")

    if isinstance(data, dict) and len(data):
        category_instance = GoodsCategory()
        category_instance.code = data["code"]
        category_instance.name = data["name"]
        category_instance.category_type = depth
        if category_pro:
            category_instance.parent_category = category_pro
        category_instance.save()

        next_node = data.get('sub_categorys', '')
        if isinstance(next_node, list):
            for node in next_node:
                deal_category(node, depth + 1, category_instance)

if isinstance(row_data, list):
    for item in row_data:
        deal_category(item, 1, None)