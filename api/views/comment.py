from django.views import View
from django.http import JsonResponse
from django import forms
from api.views.login import clean_form
from app01.models import Comment

class CommentView(View):

    # 发布评论
    def post(self, request, nid):
        # 必需的内容：文章id 用户 评论的内容
        res = {
            'msg': 'Comment post successfully',
            'code': 412,
            'self': None
        }
        data = request.data
        if not request.user.username:  # 检查用户是否登录
            res['msg'] = 'Please login first'
            return JsonResponse(res)

        # 验证评论为空时
        content = data.get('content')
        if not content:
            res['msg'] = 'Please enter your comment'
            res['self'] = 'content'
            return JsonResponse(res)

        # 文章评论校验成功
        Comment.objects.create(
            content=content,
            user=request.user,
            article_id=nid
        )
        res['code'] = 0
        return JsonResponse(res)