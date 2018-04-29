"""normalshop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# from django.contrib import admin
from django.urls import path, re_path, include
import xadmin
from normalshop.settings import MEDIA_ROOT
from django.views.static import serve

from rest_framework.documentation import include_docs_urls
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken import views
from rest_framework_jwt.views import obtain_jwt_token
from django.views.generic import TemplateView

from goods.views import GoodsListViewSet, GoodsCategoryViewSet, BannerViewSet, IndexCategoryViewSet
from users.views import SmsCodeViewSet, UserViewSet
from user_operation.views import UserFavViewSet, LeavingMessageViewSet, AddressViewSet
from trade.views import ShoppingCartViewSet, OrderViewSet
from trade.views import AlipayView

router = DefaultRouter()
# 配置goods的url
router.register('goods', GoodsListViewSet, base_name='goods')
# 分类
router.register('categorys', GoodsCategoryViewSet, base_name='categorys')
# 短信验证码
router.register('codes', SmsCodeViewSet, base_name='codes')
# 用户注册登录
router.register('users', UserViewSet, base_name='users')
# 用户收藏
router.register('userfavs', UserFavViewSet, base_name='userfavs')
# 用户留言
router.register('messages', LeavingMessageViewSet, base_name='messages')
# 收货地址
router.register('address', AddressViewSet, base_name='address')
# 购物车
router.register('shopcarts', ShoppingCartViewSet, base_name='shopcarts')
# 订单
router.register('orders', OrderViewSet, base_name='orders')
# 首页轮播图
router.register('banners', BannerViewSet, base_name='banners')
# 首页推荐商品
router.register('indexgoods', IndexCategoryViewSet, base_name='indexgoods')

urlpatterns = [
    path('xadmin/', xadmin.site.urls),
    # path('goods/', include('goods.urls')),
    path('', include(router.urls)),
    # 配置上传文件的访问处理函数
    re_path(r'^media/(?P<path>.*)$', serve, {"document_root": MEDIA_ROOT}),
    path('docs/', include_docs_urls(title="通用生鲜")),
    path('api-auth/', include('rest_framework.urls')),
    # drf自带的认证模式
    path('api-token-auth/', views.obtain_auth_token),
    # jwt认证接口
    path('login/', obtain_jwt_token),
    path('alipay/return/', AlipayView.as_view(), name="alipay"),
    # 第三方登录
    path('', include('social_django.urls', namespace='social'))
    # path('index/', TemplateView.as_view(template_name="index.html"), name="index")
]
