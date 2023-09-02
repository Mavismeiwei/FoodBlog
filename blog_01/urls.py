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
from app01 import views
from django.conf import settings
from django.views.static import serve

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index),
    path('news/', views.news),
    path('login/', views.login),
    path('login/random_code/', views.get_random_code),
    path('register/', views.register),
    path('logout/', views.logout),

    path('backend/', views.backend),  # backend user center
    path('backend/add_article/', views.add_article),  # backend add article


    re_path(r'^article/(?P<nid>\d+)/', views.article),  # article detail page

    # distribute all requests that start with api to api urls.py
    re_path(r'^api/', include('api.urls')),  # distribute the path

    # media configuration: user upload path configuration
    re_path(r'media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
]
