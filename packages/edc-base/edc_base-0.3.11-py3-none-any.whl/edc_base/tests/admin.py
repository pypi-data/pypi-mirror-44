from django.contrib.admin import register, ModelAdmin

from .admin_site import edc_base_admin
from .models import TestBaseModel


@register(TestBaseModel, site=edc_base_admin)
class TestBaseModelAdmin(ModelAdmin):
    pass
