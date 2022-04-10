from django.contrib import admin

from .models import Account, DataRegion, AccountDataType


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ('name', 'active', )
    search_fields = ('name', )


@admin.register(DataRegion)
class DataRegionAdmin(admin.ModelAdmin):
    pass


@admin.register(AccountDataType)
class AccountDataTypeAdmin(admin.ModelAdmin):
    pass
