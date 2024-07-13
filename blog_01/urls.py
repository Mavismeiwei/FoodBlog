"""
URL configuration for blog_01 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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

from django.urls import path, include, re_path
from django.contrib import admin
from app01.views import index
from app01.views import backend
from django.conf import settings
from django.views.static import serve

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index.index),
    path('news/', index.news),
    path('moods/', index.moods),

    # 搜索
    path('search/', index.search),

    # 登录注册
    path('login/', index.login),
    path('login/random_code/', index.get_random_code),
    path('register/', index.register),
    path('logout/', index.logout),
    re_path(r'^article/(?P<nid>\d+)/', index.article),  # article detail page

    # 后台路由
    path('backend/', backend.backend),  # backend user center
    path('backend/add_article/', backend.add_article),  # backend add article
    path('backend/edit_avatar/', backend.edit_avatar),  # backend edit avatar
    path('backend/edit_password/', backend.edit_password),  # backend update password

    path('backend/avatar_list/', backend.avatar_list),  # 头像列表
    path('backend/cover_list/', backend.cover_list),  # 封面列表
    re_path(r'^backend/edit_article/(?P<nid>\d+)/', backend.edit_article),  # 后台文章编辑


    # distribute all requests that start with api to api urls.py
    re_path(r'^api/', include('api.urls')),  # distribute the path

    # media configuration: user upload path configuration
    re_path(r'media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
]
