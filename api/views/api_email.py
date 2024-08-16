from django.core.mail import send_mail
from django.views import View
from django.http import JsonResponse
from django import forms
from api.views.login import clean_form
import random
from blog_01 import settings
from django.core.handlers.wsgi import WSGIRequest
import time
from threading import Thread
from app01.models import UserInfo
from api.models import Email

class EmailForm(forms.Form):
    email = forms.EmailField(error_messages={'required': 'Please enter email', "invalid": 'Please enter valid email.'})

    # 邮箱绑定验证 检查邮箱是否已经被绑定
    def clean_email(self):
        email = self.cleaned_data['email']
        user = UserInfo.objects.filter(email=email)
        if user:
            self.add_error('email', 'This email address is already registered.')
        return email

class ApiEmail(View):
    def post(self, request:WSGIRequest):
        res = {
            'code': 333,
            'msg': 'Send code to your email successfully!',
            'self': None
        }
        form = EmailForm(request.data)
        if not form.is_valid():
            res['self'], res['msg'] = clean_form(form)
            return JsonResponse(res)

        # 校验验证码有效性时间 去session里面读取
        valid_email_obj = request.session.get('valid_email_obj')
        if valid_email_obj:
            time_stamp = valid_email_obj['time_stamp']
            now_stamp = time.time()
            # 判断时间差是否超过2分钟
            if (now_stamp - time_stamp) < 60:
                res['msg'] = 'Frequent Requests!'
                return JsonResponse(res)

        # 发送邮箱验证码 设置超时时间
        # 生成6位随机验证码
        valid_email_code = ''.join(random.sample('0123456789', 6))
        request.session["valid_email_obj"] = {
            'code': valid_email_code,
            'email': form.cleaned_data['email'],
            'time_stamp': time.time()
        }

        Thread(target=send_mail,
               args=(
                "[Mimi's Food Blog] Verify your email address",
                f"[Mimi's Food Blog] Use this code {valid_email_code} to bind your email with your account. The code is valid for 5 minutes ",
                settings.EMAIL_HOST_USER,
                [form.cleaned_data.get('email')], False)).start()
        Email.objects.create(
            email=form.cleaned_data.get('email'),
            content='Complete Information'
        )

        res['code'] = 0
        return JsonResponse(res)