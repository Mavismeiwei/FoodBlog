from django.views import View
from django.http import JsonResponse
from app01.models import Avatars, Cover, UserInfo, History
from django import forms
from api.views.login import clean_form
import datetime

class HistoryForm(forms.Form):
    title = forms.CharField(error_messages={'required': 'Please enter the event title!'})
    content = forms.CharField(error_messages={'required': 'Please enter the event content!'})
    create_date = forms.CharField(required=False)
    drawing = forms.CharField(required=False)

    def clean_create_date(self):
        create_date = self.cleaned_data['create_date']
        if not create_date:
            create_date = datetime.date.today()
            return create_date
        date = datetime.datetime.strptime(create_date.split('T')[0], '%Y-%m-%d').date()
        return date


class HistoryView(View):
    def post(self, request, **kwargs):
        res = {
            'msg': 'Event posted successfully！',
            "code": 412,
            "self": None,
        }
        if not request.user.is_superuser:
            res['msg'] = 'Only admin has the authorization for this action!'
            return JsonResponse(res)
        data = request.data

        form = HistoryForm(data)
        if not form.is_valid():
            res['self'], res['msg'] = clean_form(form)
            return JsonResponse(res)
        res['code'] = 0
        nid = kwargs.get('nid')
        if nid:
            # 编辑操作
            history_query = History.objects.filter(nid=nid)
            history_query.update(**form.cleaned_data)
            res['msg'] = 'Event Updated successfully!'
            return JsonResponse(res)
        History.objects.create(**form.cleaned_data)
        return JsonResponse(res)


    def delete(self, request, nid):
        res = {
            'msg': 'Event posted Successfully！',
            "code": 412,
        }
        if not request.user.is_superuser:
            res['msg'] = 'Only admin has the authorization for this action!'
            return JsonResponse(res)
        history_query = History.objects.filter(nid=nid)
        history_query.delete()
        res['code'] = 0
        return JsonResponse(res)