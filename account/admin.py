from django.contrib import admin

from .models import Account, DataRegion, AccountDataType


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ('name', 'active', )
    search_fields = ('name', )
    filter_horizontal = ('data_type', 'region', )


@admin.register(DataRegion)
class DataRegionAdmin(admin.ModelAdmin):
    pass


@admin.register(AccountDataType)
class AccountDataTypeAdmin(admin.ModelAdmin):
    pass
