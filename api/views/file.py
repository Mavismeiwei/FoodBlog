from django.views import View
from django.http import JsonResponse
from app01.models import Avatars, Cover
from django.core.files.uploadedfile import InMemoryUploadedFile
from app01.models import avatar_delete, cover_delete

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
        avatar_delete(avatar_query.first())
        avatar_query.delete()

        res['code'] = 0
        return JsonResponse(res)

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
            cover_delete(cover_query.first())
            cover_query.delete()

            res['code'] = 0
            return JsonResponse(res)

