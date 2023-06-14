from django.contrib import admin

from .models import Account, DataRegion, AccountDataType


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "active",
        "access_expiration",
    )
    search_fields = ("name",)
    ordering = ("-access_expiration",)
    filter_horizontal = (
        "data_type",
        "region",
    )
    actions = ["update_active", "update_request_count", "create_token"]

    @admin.action(description="Обновить статусы")
    def update_active(self, request, queryset):
        for account in queryset:
            account.check_active()

    @admin.action(description="Создать токены")
    def create_token(self, request, queryset):
        for account in queryset:
            account.create_token()

    @admin.action(description="Принудительно обнулить счетчик запросов")
    def update_request_count(self, request, queryset):
        for account in queryset:
            account.request_day_count = 0
            account.request_month_count = 0
            account.save()


@admin.register(DataRegion)
class DataRegionAdmin(admin.ModelAdmin):
    pass


@admin.register(AccountDataType)
class AccountDataTypeAdmin(admin.ModelAdmin):
    pass
