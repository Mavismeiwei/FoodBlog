from django.views import View
from django.http import JsonResponse
from api.views.login import clean_form
from app01.models import Avatars, Moods, MoodComment
import random
from django.db.models import F
from django import forms

class AddMoodsForm(forms.Form):
    name = forms.CharField(error_messages={'required': 'Please enter your username!'})
    content = forms.CharField(error_messages={'required': 'Please enter the mood content!'})
    avatar_id = forms.IntegerField(required=False)
    drawing = forms.CharField(error_messages=False)  # 心情配图可以为空

    def clean_avatar_id(self):
        avater_id = self.cleaned_data.get('avatar_id')
        if avater_id:
            return avater_id

        # 若用户未选择头像 则随机选择头像
        avatar_list = [i.nid for i in Avatars.objects.all()]
        avatar_id = random.choice(avatar_list)
        return avatar_id

class MoodsView(View):
    def post(self, request):
        res = {
            'msg': 'Post Mood Succeed!',
            'code': 412,
            'self': None,
        }
        data = request.data

        form = AddMoodsForm(data)
        if not form.is_valid():
            res['self'], res['msg'] = clean_form(form)
            return JsonResponse(res)

        Moods.objects.create(**form.cleaned_data)

        res['code'] = 0
        return JsonResponse(res)
