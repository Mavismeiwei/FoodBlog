from django import template

# register
register = template.Library()

# set the filter
# @register.filter
# def add1(item):
#     return int(item) + 1

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
