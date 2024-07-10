from django.views import View
from django.http import JsonResponse
from markdown import markdown
from pyquery import PyQuery
from app01.models import Tags, Articles, Cover
from django import forms
from api.views.login import clean_form
import random
from django.db.models import F

# 添加文章或编辑文章的验证
class AddArticleForm(forms.Form):
    title = forms.CharField(error_messages={'required': 'Please input the title!'})
    content = forms.CharField(error_messages={'required': 'Please input the content!'})
    abstract = forms.CharField(required=False)  # 不进行为空验证
    cover_id = forms.IntegerField(required=False)

    category = forms.IntegerField(required=False)
    pwd = forms.CharField(required=False)
    recommend = forms.BooleanField(required=False)
    status = forms.IntegerField(required=False)

    word = forms.BooleanField(required=False)  # 文章字数

    # 全局钩子主要检验category和pwd
    def clean(self):
        category = self.cleaned_data['category']
        if not category:
            self.cleaned_data.pop('category')

        pwd = self.cleaned_data['pwd']
        if not pwd:
            self.cleaned_data.pop('pwd')


    # 文章简介优化
    def clean_abstract(self):
        abstract = self.cleaned_data['abstract']
        if abstract:
            return abstract
        # 截取正文的前30个字符
        content = self.cleaned_data.get('content')
        if content:
            abstract = PyQuery(markdown(content)).text()[:100]
            return abstract

    # 文章封面
    def clean_cover_id(self):
        cover_id = self.cleaned_data['cover_id']
        if cover_id:  # 用户选择封面则返回对应封面
            return cover_id
        # 未选择特定封面则随机选择一个封面
        cover_set = Cover.objects.all().values('nid')
        cover_id = random.choice(cover_set)['nid']
        return cover_id

# 添加Tag方法 需要检验当前tag是否存在与Tags列表中
def add_article_tags(tags, article_obj):
    for tag in tags:
        if tag.isdigit():
            article_obj.tag.add(tag)   # 如果tag存在 则更新tag和文章多对多的关联
        else:   # tag不存在与当前列表中, 则先创建一个tag新对象再将其与文章对象进行关联
            tag_obj = Tags.objects.create(title=tag)
            article_obj.tag.add(tag_obj.nid)

# 添加或编辑文章
class ArticleView(View):
    # 添加文章
    def post(self, request):
        res = {
            'msg': 'Post Succeed!',
            'code': 412,
            'data': None
        }

        data = request.data
        data['status'] = 1

        form = AddArticleForm(data)
        if not form.is_valid():
            res['self'], res['msg'] = clean_form(form)
            return JsonResponse(res)
        # 校验通过
        form.cleaned_data['author'] = 'Mimi'
        form.cleaned_data['source'] = 'Mimi Food Blog'
        article_obj = Articles.objects.create(**form.cleaned_data)
        # 文章标签操作
        tags = data.get('tags')
        # 添加标签
        add_article_tags(tags, article_obj)

        res['data'] = article_obj.nid
        res['code'] = 0
        return JsonResponse(res)

    # 编辑文章
    def put(self, request, nid):
        res = {
            'msg': 'Edit Succeed!',
            'code': 412,
            'data': None
        }

        # 验证article id是否存在
        article_query = Articles.objects.filter(nid=nid)
        if not article_query:
            res['msg'] = 'Error Request'
            return JsonResponse(res)
        data = request.data
        data['status'] = 1

        form = AddArticleForm(data)
        if not form.is_valid():
            res['self'], res['msg'] = clean_form(form)
            return JsonResponse(res)
        # 校验通过
        form.cleaned_data['author'] = 'Mimi'
        form.cleaned_data['source'] = 'Mimi Food Blog'
        article_query.update(**form.cleaned_data)

        # 标签修改操作
        tags = data.get('tags')
        article_query.first().tag.clear()  # 清空所有的标签
        # 添加标签
        add_article_tags(tags, article_query.first())

        res['data'] = article_query.first().nid
        res['code'] = 0
        return JsonResponse(res)

# 文章点赞
class ArticleDiggView(View):
    def post(self, request, nid):
        # nid 评论id
        res = {
            'msg': 'Article Like successfully',
            'code': 412,
            "data": 0,  # 当前评论点赞数量
        }

        comment_query = Articles.objects.filter(nid=nid)
        comment_query.update(digg_count=F('digg_count') + 1)

        digg_count = comment_query.first().digg_count

        res['code'] = 0
        res['data'] = digg_count
        return JsonResponse(res)

# 文章收藏
class ArticleCollectsView(View):
    def post(self, request, nid):
        # 判断登录
        res = {
            'msg': 'Article Collect successfully',
            'code': 412,
            "isCollects": True,  # 用data去判断当前文章收藏状态
            "data": 0  # 默认收藏数为0
        }

        if not request.user.username:  # 检查用户是否登录
            res['msg'] = 'Please login first'
            return JsonResponse(res)

        # 再次点击收藏按钮变为取消收藏: 判断用户是否已收藏文章
        flag = request.user.collects.filter(nid=nid)
        num = 1
        res['code'] = 0
        if flag:  # flag不为空说明已收藏
            res['msg'] = 'Cancel collection successfully'
            res['isCollects'] = False  # 取消收藏修改收藏状态
            request.user.collects.remove(nid)
            num = -1  # 取消收藏的话num为-1
            pass
        else:
            request.user.collects.add(nid)

        article_query = Articles.objects.filter(nid=nid)
        article_query.update(collects_count=F('collects_count') + num)  # 更新收藏文章数
        collects_count = article_query.first().collects_count
        res["data"] = collects_count
        return JsonResponse(res)