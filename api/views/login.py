from django import forms
from django.contrib import auth
from app01.models import UserInfo, Avatars
from django.views import View
from django.http import JsonResponse
import random

class LoginBaseForm(forms.Form):
    # input string
    name = forms.CharField(error_messages={'required': 'Please Enter the User Email'})  # string input
    password = forms.CharField(error_messages={'required': 'Please Enter the Password'})  # string input
    code = forms.CharField(error_messages={'required': 'Please Enter the Validation Code'})  # string input

    # rewrite init method
    def __init__(self, *args, **kwargs):
        # set the validation check
        self.request = kwargs.pop('request', None)  # pop the request, if not exist return None
        super().__init__(*args, **kwargs)

    # regional hook to check the validation code
    def clean_code(self):
        code: str = self.cleaned_data.get('code')
        valid_code: str = self.request.session.get(
            'valid_code')  # valid_code: validation code, code: current input code
        # code match check
        if code.upper() != valid_code.upper():
            self.add_error('code', 'Validation Code Error')
        return self.cleaned_data

# login validation check
class LoginForm(LoginBaseForm):

    # Global hook: get the user name and password
    def clean(self):
        name = self.cleaned_data.get('name')
        password = self.cleaned_data.get('password')

        user = auth.authenticate(username=name, password=password)
        if not user:
            # add the single error information
            self.add_error('password', 'User Email and Password Not Match')
            return self.cleaned_data
        # store the user information in the cleaned_data
        self.cleaned_data['user'] = user
        return self.cleaned_data

# register validation check
class RegisterForm(LoginBaseForm):
    re_password = forms.CharField(error_messages={'required': 'Please Enter the Password Again'})

    # check if the password and re_password match
    def clean(self):
        password = self.cleaned_data.get('password')
        re_password = self.cleaned_data.get('re_password')
        if password != re_password:
            self.add_error('re_password', 'Password Not Match')
        return self.cleaned_data

    # check username can not be duplicated
    def clean_name(self):
        name = self.cleaned_data.get('name')
        user_query = UserInfo.objects.filter(username=name)
        if user_query:
            self.add_error('name', 'This Email Has Been Used')
        return self.cleaned_data


# login error function
def clean_form(form):
    err_dict: dict = form.errors
    # get all the wrong input name list, get the first empty input each time
    err_valid = list(err_dict.keys())[0]
    err_msg = err_dict[err_valid][0]
    return err_valid, err_msg

# CBV
class LoginView(View):
    def post(self, request):
        res = {
            'code': 425,
            'msg': "Login Successfully",
            'self': None
        }

        # check the user input not empty
        form = LoginForm(request.data, request=request)  # pass the parameter request to the init method
        if not form.is_valid():  # empty check not valid
            res['self'], res['msg'] = clean_form(form)
            return JsonResponse(res)

        # Get the data and complete login operation
        user = form.cleaned_data.get('user')
        auth.login(request, user)
        res['code'] = 0  # match: state -> 0
        return JsonResponse(res)


class RegisterView(View):
    def post(self, request):
        res = {
            'code': 425,
            'msg': "Registered Successfully",
            'self': None
        }
        form = RegisterForm(request.data, request=request)
        if not form.is_valid():
            res['self'], res['msg'] = clean_form(form)
            return JsonResponse(res)

        # user UserInfo to create a new user object
        user = UserInfo.objects.create_user(
            username=request.data.get('name'),
            password=request.data.get('password'))

        # 注册成功随机选择头像
        avater_list = [i.nid for i in Avatars.objects.all()]
        user.avatar_id=random.choice(avater_list)
        user.save()

        # login after registered
        auth.login(request, user)
        res['code'] = 0  # sign in successfully message
        return JsonResponse(res)