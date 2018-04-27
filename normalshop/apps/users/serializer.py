# _*_ coding:utf-8 _*_
__author__ = 'zjty'
__date__ = '2018/4/26 下午4:43'
import re
from datetime import datetime, timedelta
from django.contrib.auth import get_user_model

from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from normalshop.settings import REGEX_MOBILE
from .models import VerifyCode

User = get_user_model()


class SmsSerializer(serializers.Serializer):
    mobile = serializers.CharField(max_length=11)

    def validated_mobile(self, date):
        """
        验证手机号码
        :param date:
        :return:
        """
        # 手机号码是否合法
        if not re.match(REGEX_MOBILE, date):
            raise serializers.ValidationError("手机号不合法")

        # 手机是否注册
        if User.objects.filter(mobile=date).count():
            raise serializers.ValidationError("用户已经存在")

        # 验证发送频率
        one_mintes_ago = datetime.now() - timedelta(hours=0, minutes=1, seconds=0)
        if VerifyCode.objects.filter(add_time__gt=one_mintes_ago, mobile=date):
            raise serializers.ValidationError("发送过于频繁，请在60s之后发送")

        return date


class UserRegSerilizer(serializers.ModelSerializer):
    code = serializers.CharField(required=True, max_length=4, min_length=4, label="验证码", write_only=True,
                                 error_messages= {
                                     "blank": "请输入验证码",
                                     "required": "请输入验证码",
                                     "max_length": "验证码格式错误",
                                     "min_length": "验证码格式错误",
                                 },
                                 help_text="验证码")

    username = serializers.CharField(label="用户名", required=True, allow_blank=False,
                                     validators=[UniqueValidator(queryset=User.objects.all(), message="用户已存在")])

    password = serializers.CharField(
        style={'input_type': 'password'},
        label="密码",
        write_only=True,
        error_messages= {
            "blank": "请输入密码",
            "required": "请输入密码",
        }
    )

    def create(self, validated_data):
        user = super(UserRegSerilizer, self).create(validated_data=validated_data)
        user.set_password(validated_data["password"])
        user.save()
        return user

    def validate_code(self, code):
        verify_records = VerifyCode.objects.filter(mobile=self.initial_data["username"]).order_by("-add_time")
        if verify_records:
            last_code = verify_records[0]
            five_mintes_ago = datetime.now() - timedelta(hours=0, minutes=5, seconds=0)
            if five_mintes_ago < last_code.add_time:
                raise serializers.ValidationError("验证码已过期")
            if last_code.code != code:
                raise serializers.ValidationError("验证码错误")
        else:
            raise serializers.ValidationError("验证码错误")

    def validate(self, attrs):
        attrs["mobile"] = attrs["username"]
        del attrs["code"]
        return attrs

    class Meta:
        model = User
        fields = ("username", "code", "mobile", "password")
