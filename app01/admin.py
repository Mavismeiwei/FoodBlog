from django.contrib import admin
from app01.models import Articles   # articles tables
from app01.models import Tags   # articles tags table
from app01.models import Cover   # articles covers table
from app01.models import Comment  # 文章评论表
from app01.models import Avatars  # 用户头像
from app01.models import UserInfo  # 用户

# Register your models here.
admin.site.register(Articles)
admin.site.register(Tags)
admin.site.register(Cover)
admin.site.register(Comment)
admin.site.register(Avatars)
admin.site.register(UserInfo)