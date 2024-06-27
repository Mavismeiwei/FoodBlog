from django.shortcuts import render, HttpResponse, redirect
from django.http import JsonResponse
from app01.utils.random_code import random_code
from django.contrib import auth
from app01.models import UserInfo
from app01.models import Articles, Tags, Cover
import json


# Create your views here.
def index(request):
    return render(request, 'index.html', {"request": request})

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

    return render(request, 'backend/edit_article.html', locals())