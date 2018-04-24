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


from goods.models import Goods, GoodsCategory, GoodsImage

from db_tools.data.product_data import row_data


def deal_product(data):
    for goods_detail in data:
        goods = Goods()
        goods.name = goods_detail["name"]
        goods.market_price = float(int(goods_detail["market_price"].replace("￥", "").replace("元", "")))
        goods.shop_price = float(int(goods_detail["sale_price"].replace("￥", "").replace("元", "")))
        goods.goods_brief = goods_detail["desc"] if goods_detail["desc"] is not None else ""
        goods.goods_desc = goods_detail["goods_desc"] if goods_detail["goods_desc"] is not None else ""
        goods.goods_front_image = goods_detail["images"][0] if goods_detail["images"] else ""

        category_name = goods_detail["categorys"][-1]
        category = GoodsCategory.objects.filter(name=category_name)
        if category:
            goods.category = category[0]
        goods.save()

        for goods_image in goods_detail["images"]:
            goods_image_instance = GoodsImage()
            goods_image_instance.image = goods_image
            goods_image_instance.goods = goods
            goods_image_instance.save()

deal_product(row_data)
