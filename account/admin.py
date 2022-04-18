from django.contrib import admin, messages

from .models import Account, DataRegion, AccountDataType


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ('name', 'active', 'access_expiration', )
    search_fields = ('name', )
    ordering = ('-access_expiration', )
    filter_horizontal = ('data_type', 'region', )
    actions = ['update_active']

    @admin.action(description='Обновить статусы')
    def update_active(self, request, queryset):
        for account in queryset:
            account.check_active()


@admin.register(DataRegion)
class DataRegionAdmin(admin.ModelAdmin):
    pass


@admin.register(AccountDataType)
class AccountDataTypeAdmin(admin.ModelAdmin):
    pass
