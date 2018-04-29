# _*_ coding:utf-8 _*_
__author__ = 'zjty'
__date__ = '2018/4/27 下午6:57'
from rest_framework import serializers
import re
import time

from normalshop.settings import REGEX_MOBILE
from goods.serializer import GoodsSerializer
from .models import ShoppingCart, OrderInfo, OrderGoods
from goods.models import Goods
from utils.alipay import AliPay
from normalshop.settings import private_key_path, ali_pub_key_path, ALIPAY_DEBUG, RETURN_URL, APP_NOTIFY_URL, APP_ID


class ShopCarDetailSerializer(serializers.ModelSerializer):
    goods = GoodsSerializer(many=False)

    class Meta:
        model = ShoppingCart
        fields = "__all__"


class ShoppingCartSerializer(serializers.Serializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    nums = serializers.IntegerField(required=True, label="数量", min_value=1,
                                    error_messages={
                                        "min_value": "商品数量不能小于一",
                                        "required": "请选择购买数量"
                                    })
    goods = serializers.PrimaryKeyRelatedField(required=True, label="商品", queryset=Goods.objects.all())

    def create(self, validated_data):
        user = self.context["request"].user
        nums = validated_data["nums"]
        goods = validated_data["goods"]
        leave_goods = Goods.objects.get(id=goods.id)
        if leave_goods.goods_num - nums <= 0:
            raise serializers.ValidationError("商品库存不足")

        existed = ShoppingCart.objects.filter(goods=goods, user=user)
        if existed:
            existed = existed[0]
            existed.nums += nums
            existed.save()
        else:
            existed = ShoppingCart.objects.create(**validated_data)
        return existed

    def update(self, instance, validated_data):
        leave_goods = Goods.objects.get(id=instance.goods.id)
        diff_nums = validated_data["nums"] - instance.nums
        if leave_goods.goods_num - diff_nums <= 0:
            raise serializers.ValidationError("商品库存不足")
        instance.nums = validated_data["nums"]
        instance.save()
        return instance


class OrderSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    pay_status = serializers.CharField(read_only=True)
    trade_no = serializers.CharField(read_only=True)
    order_sn = serializers.CharField(read_only=True)
    pay_time = serializers.DateTimeField(read_only=True, format='%Y-%m-%d %H:%M:%S')
    add_time = serializers.DateTimeField(read_only=True, format='%Y-%m-%d %H:%M:%S')
    alipay_url = serializers.SerializerMethodField(read_only=True)

    def get_alipay_url(self, obj):
        alipay = AliPay(
            appid=APP_ID,
            app_notify_url=APP_NOTIFY_URL,
            app_private_key_path=private_key_path,
            alipay_public_key_path=ali_pub_key_path,  # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
            debug=ALIPAY_DEBUG,  # 默认False,
            return_url=RETURN_URL
        )

        url = alipay.direct_pay(
            subject=obj.order_sn,
            out_trade_no=obj.order_sn,
            total_amount=obj.order_mount,
        )
        re_url = "https://openapi.alipaydev.com/gateway.do?{data}".format(data=url)

        return re_url

    def generate_order_sn(self):
        # 当前时间+userid+随机数
        from random import Random
        random_ins = Random()
        order_sn = "{time_str}{userid}{ranstr}".format(time_str=time.strftime("%Y%m%d%H%M%S"),
                                                       userid=self.context["request"].user.id,
                                                       ranstr=random_ins.randint(10, 99))

        return order_sn

    def validate(self, attrs):
        attrs["order_sn"] = self.generate_order_sn()
        return attrs

    class Meta:
        model = OrderInfo
        fields = "__all__"
        # fields = ("id", "order_sn", "trade_no", "pay_status", "post_script", "order_mount",
        #           "pay_time", "address", "signer_name", "singer_mobile")


class OrderGoodsSerialzier(serializers.ModelSerializer):
    goods = GoodsSerializer(many=False)

    class Meta:
        model = OrderGoods
        fields = "__all__"


class OrderDetailSerializer(serializers.ModelSerializer):
    goods = OrderGoodsSerialzier(many=True)
    alipay_url = serializers.SerializerMethodField(read_only=True)

    def get_alipay_url(self, obj):
        alipay = AliPay(
            appid=APP_ID,
            app_notify_url=APP_NOTIFY_URL,
            app_private_key_path=private_key_path,
            alipay_public_key_path=ali_pub_key_path,  # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
            debug=ALIPAY_DEBUG,  # 默认False,
            return_url=RETURN_URL
        )

        url = alipay.direct_pay(
            subject=obj.order_sn,
            out_trade_no=obj.order_sn,
            total_amount=obj.order_mount,
        )
        re_url = "https://openapi.alipaydev.com/gateway.do?{data}".format(data=url)

        return re_url

    class Meta:
        model = OrderInfo
        fields = "__all__"

