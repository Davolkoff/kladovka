from django.contrib import admin
from core.models import Container, ManagerCallRequest
from .models import *


class ManagerCallRequestAdmin (admin.ModelAdmin):
    list_display = [field.name for field in ManagerCallRequest._meta.fields]

    class Meta:
        model = ManagerCallRequest


admin.site.register(Container)
admin.site.register(ManagerCallRequest, ManagerCallRequestAdmin)