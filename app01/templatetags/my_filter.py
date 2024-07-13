import datetime
from app01.models import Tags, Avatars
from django import template
import json
import pendulum
# 注册
register = template.Library()

# 判断用户是否收藏了文章
@register.filter
def is_user_collects(article, request):
    # 用户登录判断
    if str(request.user) == 'AnonymousUser':  # 用户未登录的话
        return ''
    if article in request.user.collects.all():  # 文章收藏的话 return True
        return 'show'  # 已收藏的话那就返回show这个class
    return ''  # 否则返回空

# 判断搜索页面是否搜索到了文章内容
@register.filter
def is_article_list(article_list):
    if len(article_list):
        return 'search_content'
    return 'no_content'

# IP地址过滤器
@register.filter
def json_loads(value):
    try:
        return json.loads(value)
    except (ValueError, TypeError):
        return {}

# 时间格式化处理
@register.filter
def date_format(date: datetime.datetime):
    pendulum.set_locale('en')  # 语言设置为英文
    tz = pendulum.now().tz
    time_difference = pendulum.parse(date.strftime('%Y-%m-%d %H:%M:%S'), tz=tz).diff_for_humans()
    return time_difference

# 头像使用总和
@register.filter
def to_calculate_avatar(avatar: Avatars):
    count = avatar.moodcomment_set.count() + avatar.moods_set.count() + avatar.userinfo_set.count()
    if count:
        return ''
    return 'no_avatar'