import json

from django.views import View
from django.http import JsonResponse
from api.views.login import clean_form
from app01.models import Avatars, Moods, MoodComment
import random
from django.db.models import F
from django import forms
from api.utils.get_user_info import get_ip, get_addr_info

class AddMoodsForm(forms.Form):
    name = forms.CharField(error_messages={'required': 'Please enter your username!'})
    content = forms.CharField(error_messages={'required': 'Please enter the mood content!'})
    avatar_id = forms.IntegerField(required=False)
    drawing = forms.CharField(required=False)  # 心情配图可以为空

    def clean_avatar_id(self):
        avatar_id = self.cleaned_data.get('avatar_id')
        if avatar_id:
            return avatar_id

        # 若用户未选择头像 则随机选择头像
        avatar_list = [i.nid for i in Avatars.objects.all()]
        avatar_id = random.choice(avatar_list)
        return avatar_id

def mood_digg(model_obj, nid):
    res = {
        'msg': 'Thanks for your like!',
        'code': 412,
    }
    mood_query = model_obj.objects.filter(nid=nid)
    mood_query.update(digg_count=F('digg_count') + 1)
    res['data'] = mood_query.first().digg_count
    res['code'] = 0
    return JsonResponse(res)

class MoodsView(View):
    # 添加心情
    def post(self, request):
        res = {
            'msg': 'Post Mood Succeed!',
            'code': 412,
            'self': None,
        }
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            res['msg'] = 'Invalid JSON data'
            return JsonResponse(res)

        form = AddMoodsForm(data)
        if not form.is_valid():
            res['self'], res['msg'] = clean_form(form)
            return JsonResponse(res)

        ip = get_ip(request)
        addr = get_addr_info(ip)
        form.cleaned_data['ip'] = ip
        form.cleaned_data['addr'] = json.dumps(addr, ensure_ascii=False)  # 转换为JSON字符串

        Moods.objects.create(**form.cleaned_data)

        res['code'] = 0
        return JsonResponse(res)

    # 删除心情
    def delete(self, request, nid):
        res = {
            'msg': 'Mood deleted successfully.',
            'code': 412,
        }
        if not request.user.is_superuser:
            res['msg'] = 'Only admin can delete the mood.'
            return JsonResponse(res)
        mood_query = Moods.objects.filter(nid=nid)
        if not mood_query:
            res['msg'] = 'This mood is not exist.'
            return JsonResponse(res)

        mood_query.delete()
        res['code'] = 0
        return JsonResponse(res)

    # 心情点赞
    def put(self, request, nid):
        return mood_digg(Moods, nid)

class MoodCommentsView(View):
    # 发布心情评论
    def post(self, request, nid):
        res = {
            'msg': 'Reply Mood Succeed!',
            'code': 412,
            'self': None,
        }
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            res['msg'] = 'Invalid JSON data'
            return JsonResponse(res)

        form = AddMoodsForm(data)
        if not form.is_valid():
            res['self'], res['msg'] = clean_form(form)
            return JsonResponse(res)

        ip = get_ip(request)
        addr = get_addr_info(ip)
        form.cleaned_data['ip'] = ip
        form.cleaned_data['addr'] = json.dumps(addr, ensure_ascii=False)  # 转换为JSON字符串

        form.cleaned_data['mood_id'] = nid
        form.cleaned_data.pop('drawing', None)
        MoodComment.objects.create(**form.cleaned_data)

        Moods.objects.filter(nid=nid).update(comment_count=F('comment_count') + 1)  # 心情评论数+1
        res['code'] = 0
        return JsonResponse(res)

    # 删除心情评论
    def delete(self, request, nid):
        res = {
            'msg': 'Mood comment deleted successfully.',
            'code': 412,
            'data': 0
        }
        if not request.user.is_superuser:
            res['msg'] = 'Only admin can delete the mood.'
            return JsonResponse(res)
        mood_id = request.data.get('mood_id')
        MoodComment.objects.filter(nid=nid).delete()

        # 删除心情评论操作前进行查询
        mood_query = Moods.objects.filter(nid=mood_id)
        mood_query.update(comment_count=F('comment_count') - 1)

        res['data'] = mood_query.first().comment_count

        res['code'] = 0

        return JsonResponse(res)

    # 心情评论点赞
    def put(self, request, nid):
        return mood_digg(MoodComment, nid)