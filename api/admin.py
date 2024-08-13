from django.contrib import admin
from api.models import Email

# Admin系统注册邮件发送
class EmailAdmin(admin.ModelAdmin):
    list_display = ['email', 'content', 'create_date']

admin.site.register(Email, EmailAdmin)
