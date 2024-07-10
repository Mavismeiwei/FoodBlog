from django import template

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