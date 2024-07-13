from django.urls import path, re_path
from api.views import login, article, comment, mood, user, file

urlpatterns = [
    path('login/', login.LoginView.as_view()),  # 登录
    path('register/', login.RegisterView.as_view()),  # 注册
    path('article/', article.ArticleView.as_view()),  # 发布文章
    re_path('article/(?P<nid>\d+)/', article.ArticleView.as_view()),  # 编辑文章
    re_path('article/comment/(?P<nid>\d+)/', comment.CommentView.as_view()),  # 发布评论
    re_path('comment/digg/(?P<nid>\d+)/', comment.CommentDiggView.as_view()),  # 评论点赞

    re_path('article/digg/(?P<nid>\d+)/', article.ArticleDiggView.as_view()),  # 文章点赞
    re_path('article/collects/(?P<nid>\d+)/', article.ArticleCollectsView.as_view()),  # 文章收藏

    path('moods/', mood.MoodsView.as_view()),  # 发布心情
    re_path('moods/(?P<nid>\d+)/', mood.MoodsView.as_view()),  # 删除心情
    re_path('mood_comments/(?P<nid>\d+)/', mood.MoodCommentsView.as_view()),  # 发布心情评论

    path('edit_password/', user.EditPasswordView.as_view()),  # 用户修改密码
    path('edit_avatar/', user.EditAvatarView.as_view()),  # 修改头像

    path('upload/avatar/', file.AvatarView.as_view()),  # 后台上传头像
    re_path(r'upload/avatar/(?P<nid>\d+)/', file.AvatarView.as_view()),  # 后台删除头像

    path('upload/cover/', file.CoverView.as_view()),  # 后台上传文章封面
    re_path(r'upload/cover/(?P<nid>\d+)/', file.CoverView.as_view()),  # 后台删除文章封面
]