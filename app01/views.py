from django.shortcuts import render, HttpResponse, redirect
from django.http import JsonResponse
from app01.utils.random_code import random_code
from django.contrib import auth
from app01.models import UserInfo
from app01.models import Articles
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