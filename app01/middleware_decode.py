from django.utils.deprecation import MiddlewareMixin
import json
from django.utils.deprecation import MiddlewareMixin
from api.utils.get_user_info import get_ip
from django.core.cache import cache

# 获取在线人数Statistical
class Statistical(MiddlewareMixin):
    def process_request(self, request):
        ip = get_ip(request)  # 判断ip是否在已有的ip列表中 读取ip数量获得在线人数
        online_ips = list(cache.get('online_lips', [])) # 读取ip列表

        if online_ips:
            online_ips = list(cache.get_many(online_ips).keys())

        cache.set(ip, 0, 10)  # 超过时间 单位：秒

        if ip not in online_ips:
            online_ips.append(ip)

        cache.set("online_ips", online_ips)

        request.online_list = online_ips

# decode the data of POST request
class Md1(MiddlewareMixin):
    # Request Middleware
    def process_request(self, request):
        if request.method != 'GET' and request.META.get('CONTENT_TYPE') == 'application/json':
            data = json.loads(request.body)  # encode the data into dictionary
            request.data = data

    # Response the middleware
    def process_response(self, request, response):
        return response