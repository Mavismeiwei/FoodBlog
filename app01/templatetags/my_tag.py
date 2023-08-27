from django import template

# register
register = template.Library()

# set the filter
# @register.filter
# def add1(item):
#     return int(item) + 1

@register.inclusion_tag('my_tag/headers.html')
def banner(menu_name):
    print(menu_name)
    img_list = [
        "/static/resources/img/home/bg1.jpeg",
        "/static/resources/img/home/bg2.jpeg",
        "/static/resources/img/home/bg7.jpeg"
    ]
    return {"img_list": img_list}
