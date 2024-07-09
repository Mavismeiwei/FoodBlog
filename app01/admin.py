from django.contrib import admin
from app01.models import *
from django.utils.safestring import mark_safe

class ArticleAdmin(admin.ModelAdmin):
    # 自定义方法在django后台编辑文章页面显示文章封面
    def get_cover(self, obj):
        if obj.cover:
            return mark_safe(f'<img src="{obj.cover.url.url}" style="height:60px; border-radius: 5px;">')
        return '-'
    get_cover.short_description = 'Cover'

    # 显示所有标签
    def get_tags(self, obj):
        tag_list = ', '.join([i.title for i in obj.tag.all()])
        return tag_list
    get_tags.short_description = 'Tags'

    # 自定义方法在django后台文章页面显示文章标题并添加链接
    def get_title(self, obj):
        return mark_safe(f'<a href="/article/{obj.nid}">{obj.title}</a>')
    get_title.short_description = 'Article Title'

    # 自定义方法在django后台文章页面显示编辑和删除按钮
    def get_edit_delete_btn(self, obj):
        return mark_safe(f"""
            <a href="/backend/edit_article/{obj.nid}/" target="_blank">编辑</a>
            <a href="/admin/app01/articles/{obj.nid}/delete/" target="_blank">删除</a>
        """)
    get_edit_delete_btn.short_description = 'Action'

    # 自定义动作方法，计算文章字数
    def action_word(self, request, queryset):
        for obj in queryset:
            word = len(obj.content)
            obj.word = word
            obj.save()
    action_word.short_description = 'Count the article words'
    action_word.type = 'success'

    list_display = ['get_title', 'get_cover', 'get_tags', 'category', 'look_count', 'digg_count', 'comment_count', 'collects_count', 'word', 'change_date', 'get_edit_delete_btn']
    actions = [action_word]

# Register your models here.
admin.site.register(Articles, ArticleAdmin)
admin.site.register(Tags)
admin.site.register(Cover)
admin.site.register(Comment)
admin.site.register(Avatars)
admin.site.register(UserInfo)
