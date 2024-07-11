import requests
import re

headers = {
    "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Mobile Safari/537.36"
}

def get_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')  # 判断是否使用代理
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
        return ip
    ip = request.META.get('REMOTE_ADDR')  # 未使用代理获取ip
    return ip


def get_addr_info(ip):
    # 过滤私有IP地址
    if ip.startswith('10.') or ip.startswith('192') or ip.startswith('127'):
        return {'ct': "中国", 'prov': "内网"}

    # 构建请求URL
    url = f'https://www.ip138.com/iplookup.asp?ip={ip}&action=2'
    # 发送HTTP请求
    response = requests.get(url=url, headers=headers)
    res = response.content.decode('gbk')  # 解码GBK编码，因为ip138可能返回中文内容

    # 使用正则表达式提取结果
    result = re.findall(r'ip_result = (.*?);', res, re.S)[0]
    consequence = eval(result)  # 将结果字符串转换为字典
    addr_dict = consequence['ip_c_list'][0]

    # 移除不需要的键
    keys_to_remove = ['begin', 'end', 'idc', 'net']
    for key in keys_to_remove:
        addr_dict.pop(key, None)  # 使用pop移除键，并防止KeyError

    # 如果'area'键不存在，则移除
    if not addr_dict.get('area'):
        addr_dict.pop('area', None)

    return addr_dict


if __name__ == '__main__':
    ips = ['72.14.201.199', '36.99.136.139', '120.228.2.238', '127.0.0.1']
    for ip in ips:
        info = get_addr_info(ip)
        print(f"IP: {ip} - Info: {info}")
