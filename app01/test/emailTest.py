import os
import django
from django.core.mail import send_mail
from blog_01 import settings

if __name__ == '__main__':
    # 加载Django项目的配置信息
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "blog_01.settings")
    # 启动Django项目
    django.setup()

    send_mail(
        "[Mimi's Food Blog] Verify your email address",
        'Please click the link below to verify your email address.',
        settings.EMAIL_HOST_USER,
        ['zhang.meiwe@northeastern.edu'],
        fail_silently=False
    )
