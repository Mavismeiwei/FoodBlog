from django.urls import path, re_path
from api.views import login, article

urlpatterns = [
    path('login/', login.LoginView.as_view()),  # 登录
    path('register/', login.RegisterView.as_view()),  # 注册
    path('article/', article.ArticleView.as_view()),  # 发布文章
    re_path('article/(?P<nid>\d+)/', article.ArticleView.as_view()),  # 编辑文章

]