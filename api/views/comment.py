from django.views import View
from django.http import JsonResponse
from django import forms
from api.views.login import clean_form
from app01.models import Comment, Articles
from django.db.models import F
from api.utils.find_root_comment import find_root_comment
from app01.utils.sub_comment import find_root_sub_comment

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

        pid = data.get('pid')

        # 文章评论数加一
        Articles.objects.filter(nid=nid).update(comment_count=F('comment_count') + 1)

        # pid 不为空 说明是子评论
        if pid:
            comment_obj = Comment.objects.create(
                content=content,
                user=request.user,
                article_id=nid,
                parent_comment_id=pid
            )
            # 回复根评论 找到最终的根评论 + 1
            root_comment_obj = find_root_comment(comment_obj)
            root_comment_obj.comment_count += 1
            root_comment_obj.save()

        else:
            # 根评论
            Comment.objects.create(
                content=content,
                user=request.user,
                article_id=nid
            )
        res['code'] = 0
        return JsonResponse(res)

    def delete(self, request, nid):

        res = {
            'msg': 'Comment Deleted successfully!',
            'code': 412,
        }

        login_user = request.user
        # 评论人
        comment_query = Comment.objects.filter(nid=nid)
        comment_user = comment_query.first().user

        # 获得当前评论文章的id
        aid = request.data.get('aid')
        # 子评论的最终根评论的id
        pid = request.data.get('pid')

        # 获得当前用户进行判断： 判断当前用户若和评论人不一致 或着不是管理员
        if not (login_user == comment_user or login_user.is_superuser):
            res['msg'] = 'You could not delete this comment.'
            return JsonResponse(res)

        # 根评论删除
        lis = []
        find_root_sub_comment(comment_query.first(), lis)
        Articles.objects.filter(nid=aid).update(comment_count=F('comment_count') - len(lis) - 1)

        # 删除子评论
        if pid:
            Comment.objects.filter(nid=pid).update(comment_count=F('comment_count') - len(lis) - 1)

        comment_query.delete()
        res['code'] = 0

        return JsonResponse(res)


class CommentDiggView(View):
    def post(self, request, nid):
        # nid 评论id
        res = {
            'msg': 'Like successfully',
            'code': 412,
            "data": 0,  # 当前评论点赞数量
        }

        if not request.user.username:  # 检查用户是否登录
            res['msg'] = 'Please login first'
            return JsonResponse(res)

        comment_query = Comment.objects.filter(nid=nid)
        comment_query.update(digg_count=F('digg_count') + 1)

        digg_count = comment_query.first().digg_count
        res['code'] = 0
        res['data'] = digg_count

        return JsonResponse(res)