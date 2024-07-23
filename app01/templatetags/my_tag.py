from django import template
import re
from app01.models import Tags, Avatars, Menu
from app01.utils.search import Search
from django.utils.safestring import mark_safe

# register
register = template.Library()

@register.inclusion_tag('my_tag/headers.html')
def banner(menu_name, article=None):
    if article:
        # 说明是文章详情页面
        # 拿到文章的封面
        cover = article.cover.url.url
        img_list = [cover]
        title = article.title
        slogan_list = [article.abstract[:30]]
        return locals()

    menu_obj = Menu.objects.get(menu_title_en=menu_name)
    img_list = [i.url.url for i in menu_obj.menu_url.all()]
    menu_time = menu_obj.menu_time
    title = menu_obj.title
    slogan_list = menu_obj.abstract.replace('；', ';').replace('\n', ';').split(';')
    slogan_time = menu_obj.abstract_time
    if not menu_obj.menu_rotation:
        # 如果不轮播
        img_list = img_list[0:1]
        menu_time = 0

    if not menu_obj.rotation:
        slogan_list = slogan_list[0:1]
        slogan_time = 0

    return locals()

@register.simple_tag
# 搜索页过滤器
def generate_order_html(request, key):
    order = request.GET.get(key, '')  # 过滤器筛排序
    order_list = []
    if key == 'order':
        order_list = [
            ('', 'Recommend'),
            ('-create_date', 'Latest Release'),
            ('-look_count', 'Most Viewed'),
            ('-digg_count', 'Most Liked'),
            ('-collects_count', 'Most Collected'),
            ('-comment_count', 'Most Comments')
        ]

    elif key == 'word':
        order = request.GET.getlist(key, '')
        order_list = [
            ([''], 'All Articles'),
            (['0', '100'], '100 words'),
            (['100', '500'], '500 words'),
            (['500', '1000'], '1000 words'),
            (['1000', '2000'], '2000 words'),
            (['2000', '3000'], '3000 words')
        ]
        # 从数据库中读取tag 如果tag下对应的文章为空 不需要显示该tag
    elif key == 'tag':
        tag_list = Tags.objects.exclude(articles__isnull=True)
        order_list.append(('', 'All Tags'))
        for tag in tag_list:
            order_list.append((tag.title, tag.title))

    query_params = request.GET.copy()

    # 搜索实例化
    order = Search(
        key=key,
        order=order,
        order_list=order_list,
        query_params=query_params
    )
    return mark_safe(order.order_html())

# 动态导航
@register.simple_tag
def dynamic_navigation(request):
    path = request.path_info
    path_dict = {
        '/': 'Home',
        '/news': 'News',
        '/moods': 'Moods',
        '/history': 'History',
        '/about': 'About',
        '/sites': 'Sites'
    }
    nav_list = []
    for k, v in path_dict.items():
        if k == path:
            nav_list.append(f'<a href="{k}" class="active">{v}</a>')
            continue
        nav_list.append(f'<a href="{k}">{v}</a>')
    return mark_safe(''.join(nav_list))

# 主页生成云标签
@register.simple_tag
def generate_tag_html():
    tag_list = Tags.objects.all()[:15]
    tag_html = []
    for tag in tag_list:
        if tag.articles_set.all():
            tag_html.append(f'<li>{tag.title} <i>{tag.articles_set.count()}</i></li>')
        else:
            tag_html.append(f'<li>{tag.title}</li>')
    return mark_safe(''.join(tag_html))

# 发布心情配图
@register.simple_tag
def generate_drawing(drawing: str):
    if not drawing:
        return ''
    drawing = drawing.replace('；', ';').replace('\n', ';')
    drawing_list = drawing.split(';')
    html_s = ''
    for i in drawing_list:
        html_s += f'<img @error="img_error" src="{i}" alt="">'

    return mark_safe(html_s)

@register.simple_tag
def generate_li(content: str):
    if not content:
        return ''
    drawing = content.replace('；', ';').replace('\n', ';')
    drawing_list = drawing.split(';')
    html_s = ''
    for i in drawing_list:
        html_s += f'<li>{i}</li>'

    return mark_safe(html_s)