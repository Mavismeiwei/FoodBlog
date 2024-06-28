from django.shortcuts import render, HttpResponse, redirect
from django.http import JsonResponse
from app01.utils.random_code import random_code
from django.contrib import auth
from app01.models import UserInfo
from app01.models import Articles, Tags, Cover
import json


# Create your views here.
def index(request):
    article_list = Articles.objects.filter(status=1).order_by('-change_date')  # status为1 说明文章已发布
    recipes_list = article_list.filter(category=1)[:6]  # 获取不同category的文章
    nutrition_list = article_list.filter(category=2)[:6]
    culinary_list = article_list.filter(category=3)[:6]
    food_reviews_list = article_list.filter(category=4)[:6]
    return render(request, 'index.html', locals())

def article(request, nid):
    article_query = Articles.objects.filter(nid=nid)
    if not article_query:
        return redirect('/')   # if article not exist, return homepage
    article = article_query.first()
    return render(request, 'article.html', locals())

def news(request):
    return render(request, 'news.html')

def login(request):
    return render(request, 'login.html')

# get the random code
def get_random_code(request):
    data, valid_code = random_code()
    request.session['valid_code'] = valid_code
    return HttpResponse(data)

def register(request):
    return render(request, 'register.html')

def logout(request):
    auth.logout(request)
    return redirect('/')

def backend(request):
    if not request.user.username:  # username is empty
        return redirect('/')
    return render(request, 'backend/backend.html', locals())

def add_article(request):
    # 从Tags表中获取文章标签Tags
    tag_list = Tags.objects.all()
    # 从Covers中获得文章封面
    cover_list = Cover.objects.all()
    # 拿到所有的文章分类category_list
    category_list = Articles.category_choice  # 元组
    c_l = []
    for cover in cover_list:
        c_l.append({
            "url": cover.url.url,
            'nid': cover.nid
        })
    return render(request, 'backend/add_article.html', locals())

def edit_avatar(request):
    return render(request, 'backend/edit_avatar.html', locals())

def reset_password(request):
    return render(request, 'backend/reset_password.html', locals())

def edit_article(request, nid):
    article_obj = Articles.objects.get(nid=nid)
    tags = [str(tag.nid) for tag in article_obj.tag.all()]

    tag_list = Tags.objects.all()
    # 从Covers中获得文章封面
    cover_list = Cover.objects.all()

    tag_list = Tags.objects.all()
    # 从Covers中获得文章封面
    cover_list = Cover.objects.all()
    c_l = []
    for cover in cover_list:
        c_l.append({
            "url": cover.url.url,
            'nid': cover.nid
        })
    # 拿到所有的文章分类category_list
    category_list = Articles.category_choice  # 元组
    return render(request, 'backend/edit_article.html', locals())