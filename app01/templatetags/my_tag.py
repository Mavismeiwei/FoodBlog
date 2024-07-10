from django import template

from app01.models import Tags
from app01.utils.search import Search
from django.utils.safestring import mark_safe

# register
register = template.Library()

@register.inclusion_tag('my_tag/headers.html')
def banner(menu_name, article=None):
    img_list = [
        "/static/resources/img/home/bg1.jpeg",
        "/static/resources/img/home/bg2.jpeg",
        "/static/resources/img/home/bg7.jpeg"
    ]
    if article:  # check if current page is the article detail page
        # get the article cover
        cover = article.cover.url.url
        img_list = [cover]
        pass
    return {"img_list": img_list}

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
        '/memory': 'Memory',
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

# 发布心情配图
@register.simple_tag
def generate_drawing(drawing: str):
    if not drawing:
        return ''
    drawing = drawing.replace('；', ';').replace('\n', ';')
    drawing_list = drawing.split(';')
    html_s = ''
    for i in drawing_list:
        html_s += f'<img src="{i}" alt="">'

    return mark_safe(html_s)

