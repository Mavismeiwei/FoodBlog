from django.views import View
from django.http import JsonResponse
from django.contrib import auth

from api.views.login import clean_form
from django import forms

class EditPasswordForm(forms.Form):
    old_pwd = forms.CharField(min_length=4, error_messages={'required': 'Please enter your previous password', 'min_length': 'The length of password at least for 4.'})
    pwd = forms.CharField(min_length=4, error_messages={'required': 'Please enter your new password', 'min_length': 'The length of password at least for 4.'})
    re_pwd = forms.CharField(min_length=4, error_messages={'required': 'Please confirm your new password','min_length': 'The length of password at least for 4.'})

    # 重写init方法
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)  # pop the request, if not exist return None
        super().__init__(*args, **kwargs)

    # 检验旧密码是否正确
    def clean_old_pwd(self):
        old_pwd = self.cleaned_data['old_pwd']
        user = auth.authenticate(username=self.request.user.username, password=old_pwd)
        if not user:
            self.add_error('old_pwd', 'Previous password error.')
        return old_pwd

    def clean(self):
        pwd = self.cleaned_data.get('pwd')
        re_pwd = self.cleaned_data.get('re_pwd')
        if pwd != re_pwd:
            self.add_error('re_pwd', 'Password not match.')
        return self.cleaned_data

# 修改密码
class EditPasswordView(View):
    def post(self, request):
        res = {
            "msg": 'Password update successfully.',
            "self": None,
            "code": 414,
        }
        data = request.data
        form = EditPasswordForm(data, request=request)
        if not form.is_valid():
            # 验证不通过
            res['self'], res['msg'] = clean_form(form)
            return JsonResponse(res)
        user = request.user
        user.set_password(data['pwd'])
        user.save()
        auth.logout(request)  # 退出登录

        res['code'] = 0

        return JsonResponse(res)