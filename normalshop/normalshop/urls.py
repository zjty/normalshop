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

from goods.views import GoodsListViewSet, GoodsCategoryViewSet

router = DefaultRouter()
# 配置goods的url
router.register('goods', GoodsListViewSet, base_name='goods')
router.register('categorys', GoodsCategoryViewSet, base_name='categorys')

urlpatterns = [
    path('xadmin/', xadmin.site.urls),
    # path('goods/', include('goods.urls')),
    path('', include(router.urls)),
    # 配置上传文件的访问处理函数
    re_path(r'media/(?P<path>.*)$', serve, {"document_root": MEDIA_ROOT}),
    path('docs/', include_docs_urls(title="通用生鲜")),
    path('api-auth/', include('rest_framework.urls')),
]
