from django.shortcuts import render, HttpResponse, redirect
from app01.utils.random_code import random_code
from django.contrib import auth
from app01.models import *
from django.db.models import F
from app01.utils.sub_comment import sub_comment_list
from app01.utils.pagination import Pagination

# 主页
# Create your views here.
def index(request):
    article_list = Articles.objects.filter(status=1).order_by('-change_date')  # status为1 说明文章已发布
    recipes_list = article_list.filter(category=1)[:6]  # 获取不同category的文章
    nutrition_list = article_list.filter(category=2)[:6]
    culinary_list = article_list.filter(category=3)[:6]
    food_reviews_list = article_list.filter(category=4)[:6]

    # 使用分页器
    query_params = request.GET.copy()
    pager = Pagination(
        current_page=request.GET.get('page'),
        all_count=article_list.count(),
        base_url=request.path_info,
        query_params=query_params,
        per_page=5,
        pager_page_count=7,
    )
    article_list = article_list[pager.start:pager.end]

    return render(request, 'index.html', locals())

# 文章详情页
def article(request, nid):
    article_query = Articles.objects.filter(nid=nid)
    article_query.update(look_count=F('look_count') + 1)  # 更新浏览数量 每访问一次就+1
    if not article_query:
        return redirect('/')   # if article not exist, return homepage
    article = article_query.first()
    comment_list = sub_comment_list(nid)  # 通过文章nid得到comment_list

    return render(request, 'article.html', locals())

# 新闻页
def news(request):
    return render(request, 'news.html')

# 心情页
def moods(request):
    # 查询所有的头像
    avatar_list = Avatars.objects.all()

    # 心情搜索
    key = request.GET.get('key', '')

    mood_list = Moods.objects.filter(content__contains=key).order_by('-create_date')

    # 使用分页器
    query_params = request.GET.copy()
    pager = Pagination(
        current_page=request.GET.get('page'),
        all_count=mood_list.count(),
        base_url=request.path_info,
        query_params=query_params,
        per_page=5,
        pager_page_count=7,
    )
    mood_list = mood_list[pager.start:pager.end]

    return render(request, 'moods.html', locals())

# 搜索视图
def search(request):
    search_key = request.GET.get('key', '')  # 搜索参数
    order = request.GET.get('order', '')  # 过滤器筛排序
    tag = request.GET.get('tag', '')  # 按照标签排序
    word = request.GET.getlist('word')  # 字数多少排序参数

    query_params = request.GET.copy()
    article_list = Articles.objects.filter(title__contains=search_key)

    # 判断word参数是否为空
    if len(word) == 2:
        article_list = article_list.filter(word__range=word)
    # 文章标签
    if tag:
        article_list = article_list.filter(tag__title=tag)

    if order:  # order存在 说明点击过滤词 最多点赞/收藏/评论
        try:
            article_list = article_list.order_by(order)
        except Exception:
            pass

    # 使用分页器
    pager = Pagination(
        current_page=request.GET.get('page'),
        all_count=article_list.count(),
        base_url=request.path_info,
        query_params=query_params,
        per_page=10,
        pager_page_count=7,
    )
    article_list = article_list[pager.start:pager.end]

    return render(request, 'search.html', locals())

# 登录
def login(request):
    return render(request, 'login.html')

# get the random code
def get_random_code(request):
    data, valid_code = random_code()
    request.session['valid_code'] = valid_code
    return HttpResponse(data)

# 注册
def register(request):
    return render(request, 'register.html')

# 登出
def logout(request):
    auth.logout(request)
    return redirect('/')

# 回忆录history页
def history(request):
    history_list = History.objects.all().order_by('create_date');
    return render(request, 'history.html', locals())

# about页面
def about(request):
    return render(request, 'about.html')

# 网站导航sites页
def sites(request):
    return render(request, 'sites.html')