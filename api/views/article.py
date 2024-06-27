from django.views import View
from django.http import JsonResponse
from markdown import markdown
from pyquery import PyQuery
from app01.models import Tags, Articles, Cover
from django import forms
from api.views.login import clean_form
import random

class AddArticleForm(forms.Form):
    title = forms.CharField(error_messages={'required': 'Please input the title!'})
    content = forms.CharField(error_messages={'required': 'Please input the content!'})
    abstract = forms.CharField(required=False)  # 不进行为空验证
    cover_id = forms.IntegerField(required=False)

    category = forms.IntegerField(required=False)
    pwd = forms.CharField(required=False)
    recommend = forms.BooleanField(required=False)
    status = forms.IntegerField(required=False)

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
            abstract = PyQuery(markdown(content)).text()[:30]
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

class ArticleView(View):
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
        article_obj = Articles.objects.create(**form.cleaned_data)
        print(article_obj)

        # 文章标签操作
        tags = data.get('tags')
        # 检验当前tag是否存在与Tags列表中
        for tag in tags:
            if tag.isdigit():
                article_obj.tag.add(tag)   # 如果tag存在 则更新tag和文章多对多的关联
            else:   # tag不存在与当前列表中, 则先创建一个tag新对象再将其与文章对象进行关联
                tag_obj = Tags.objects.create(title=tag)
                article_obj.tag.add(tag_obj.nid)
        res['data'] = article_obj.nid
        res['code'] = 0
        return JsonResponse(res)
