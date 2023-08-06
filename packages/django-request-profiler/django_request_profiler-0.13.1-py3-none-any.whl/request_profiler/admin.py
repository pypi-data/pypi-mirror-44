from django.contrib import admin

from .models import RuleSet, ProfilingRecord


class RuleSetAdmin(admin.ModelAdmin):

    list_display = (
        'enabled',
        'uri_regex',
        'user_filter_type',
        'user_group_filter',
    )


class ProfilingRecordAdmin(admin.ModelAdmin):

    list_display = (
        'start_ts',
        'user',
        'session_key',
        'remote_addr',
        'http_method',
        'request_uri',
        'view_func_name',
        'response_status_code',
        'duration',
    )


admin.site.register(RuleSet, RuleSetAdmin)
admin.site.register(ProfilingRecord, ProfilingRecordAdmin)
