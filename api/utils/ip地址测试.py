import os
import json
from api.utils.get_user_info import get_addr_info

if __name__=='__main__':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', "blog_01.settings")
    import django

    django.setup()

    from app01.models import Moods

    mood_query = Moods.objects.all()
    for obj in mood_query:
        print(obj.addr, type(obj.addr))
        addr_info = get_addr_info(obj.ip)
        # 将字典转换为 JSON 字符串，不使用 Unicode 转义字符
        obj.addr = json.dumps(addr_info, ensure_ascii=False)
        obj.save()
