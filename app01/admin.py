from django.contrib import admin
from app01.models import Articles   # articles tables
from app01.models import Tags   # articles tags table
from app01.models import Cover   # articles covers table

# Register your models here.
admin.site.register(Articles)
admin.site.register(Tags)
admin.site.register(Cover)