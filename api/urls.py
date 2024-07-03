from django.urls import path, re_path
from api.views import login, article, comment

urlpatterns = [
    path('login/', login.LoginView.as_view()),  # 登录
    path('register/', login.RegisterView.as_view()),  # 注册
    path('article/', article.ArticleView.as_view()),  # 发布文章
    re_path('article/(?P<nid>\d+)/', article.ArticleView.as_view()),  # 编辑文章
    re_path('article/comment/(?P<nid>\d+)/', comment.CommentView.as_view()),  # 发布评论
    re_path('comment/digg/(?P<nid>\d+)/', comment.CommentDiggView.as_view()),  # 评论点赞

    re_path('article/digg/(?P<nid>\d+)/', article.ArticleDiggView.as_view()),  # 文章点赞
    re_path('article/collects/(?P<nid>\d+)/', article.ArticleCollectsView.as_view()),  # 文章收藏
]