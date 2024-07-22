from django.shortcuts import render, HttpResponse, redirect
from app01.models import *


# 后台用户界面
def backend(request):
    avatar_list = Avatars.objects.all()
    if not request.user.username:  # username is empty
        return redirect('/')

    # 获取当前用户的收藏文章
    user = request.user
    collects_query = user.collects.all()

    return render(request, 'backend/backend.html', locals())

# 后台文章添加页
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

# 后台头像修改
def edit_avatar(request):
    user = request.user
    sign_status = user.sign_status
    # 获取所有的头像
    avatar_list = Avatars.objects.all()

    if sign_status == 0:
        # 如果是用户名密码注册
        avatar_id = request.user.avatar.nid
    else:
        # 第三方登录
        avatar_url = request.user.avatar_url
        for i in avatar_list:
            if i.url.url == avatar_url:
                avatar_id = i.nid
    return render(request, 'backend/edit_avatar.html', locals())

# 重置密码页
def edit_password(request):
    return render(request, 'backend/edit_password.html', locals())

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

# 头像列表
def avatar_list(request):
    # 获取所有的头像
    avatar_query = Avatars.objects.all()
    return render(request, 'backend/avatar_list.html', locals())

# 文章封面
def cover_list(request):
    cover_query = Cover.objects.all()
    return render(request, 'backend/cover_list.html', locals())