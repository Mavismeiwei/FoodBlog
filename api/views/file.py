from django.views import View
from django.http import JsonResponse
from app01.models import Avatars, Cover, UserInfo
from django.core.files.uploadedfile import InMemoryUploadedFile
from app01.models import avatar_delete, cover_delete
from django.core.handlers.wsgi import WSGIRequest
from django.db.models import Q
import base64
import time
from api.utils.api_qiniu import upload_data

# 头像
class AvatarView(View):
    def post(self, request):
        # 判断文件上传类型是否合法
        res = {
            "code": 345,
            "msg": 'File upload is not valid.'
        }
        # 管理员权限认证
        if not request.user.is_superuser:
            res['msg'] = 'Only admin can delete the mood.'
            return JsonResponse(res)

        file: InMemoryUploadedFile = request.FILES.get('file')
        name: str = file.name
        # 文件类型白名单
        white_file_type = [
            'jpg', 'jpeg', 'png', 'gif', 'bmp', 'webp', 'tiff'
        ]
        if name.split('.')[-1] not in white_file_type:
            return JsonResponse(res)

        kb = file.size / 1024 / 1024
        if kb > 2:
            res['msg'] = 'The image size exceeds 2MB.'
            return JsonResponse(res)
        Avatars.objects.create(url=file)
        res['code'] = 0
        res['msg'] = 'Upload successfully!'
        return JsonResponse(res)


    # 删除头像
    def delete(self, request, nid):
        res = {
            'code': 322,
            'msg': 'Deleted successfully!'
        }

        # 管理员权限认证
        if not request.user.is_superuser:
            res['msg'] = 'Only admin can delete the mood.'
            return JsonResponse(res)

        # 使用models.py中定义好的删除头像方法
        avatar_query = Avatars.objects.filter(nid=nid)
        if not avatar_query:
            res['msg'] = 'Avatar has been deleted!'
            return JsonResponse(res)

        # 判断图片是否有人在使用
        obj: Avatars = avatar_query.first()

        userquery = UserInfo.objects.filter(Q(sign_status=1) | Q(sign_status=2))
        for user in userquery:
            if obj.url.url == user.avatar_url:
                res['msg'] = 'This avatar is being used by user.'
                return JsonResponse(res)

        avatar_delete(obj)
        avatar_query.delete()

        res['code'] = 0
        return JsonResponse(res)

# 封面
class CoverView(View):
        def post(self, request):
            # 判断文件上传类型是否合法
            res = {
                "code": 345,
                "msg": 'File upload is not valid.'
            }
            # 管理员权限认证
            if not request.user.is_superuser:
                res['msg'] = 'Only admin can delete the mood.'
                return JsonResponse(res)

            file: InMemoryUploadedFile = request.FILES.get('file')
            name: str = file.name
            # 文件类型白名单
            white_file_type = [
                'jpg', 'jpeg', 'png', 'gif', 'bmp', 'webp', 'tiff'
            ]
            if name.split('.')[-1] not in white_file_type:
                return JsonResponse(res)

            kb = file.size / 1024 / 1024
            if kb > 2:
                res['msg'] = 'The image size exceeds 2MB.'
                return JsonResponse(res)
            Cover.objects.create(url=file)
            res['code'] = 0
            res['msg'] = 'Upload successfully!'
            return JsonResponse(res)

        # 删除头像
        def delete(self, request, nid):
            res = {
                'code': 322,
                'msg': 'Deleted successfully!'
            }

            # 管理员权限认证
            if not request.user.is_superuser:
                res['msg'] = 'Only admin can delete the mood.'
                return JsonResponse(res)

            # 使用models.py中定义好的删除头像方法
            cover_query = Cover.objects.filter(nid=nid)
            if not cover_query:
                res['msg'] = 'Cover has been deleted!'
                return JsonResponse(res)
            cover_delete(cover_query.first())
            cover_query.delete()

            res['code'] = 0
            return JsonResponse(res)

# 粘贴上传
class PasteUpload(View):
    def post(self, request):
        img = request.data.get('image')
        ines = img.split('base64,')
        imgData = base64.b64decode(ines[1])
        url = upload_data(imgData)
        return JsonResponse({'url': url})
