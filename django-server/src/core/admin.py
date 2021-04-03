from django.contrib import admin
from djongo.admin import ModelAdmin
from .models import ModelHistory


@admin.register(ModelHistory)
class ModelHistoryAdmin(ModelAdmin):
    def get_readonly_fields(self, request, obj=None):
        readonly_fields = []
        if obj is not None:
            readonly_fields = [field.name for field in obj._meta.get_fields()]

        return readonly_fields

    def has_add_permission(self, request):
        return False

    def change_view(self, request, object_id, form_url='', extra_context={}):
        extra_context['show_save'] = False
        extra_context['show_save_and_continue'] = False
        return self.changeform_view(
                request, object_id, form_url, extra_context)
