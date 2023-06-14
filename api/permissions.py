from datetime import date

from rest_framework.permissions import BasePermission


class IsExpired(BasePermission):
    message = "Your account has been expired"

    def has_permission(self, request, view) -> bool:
        has_permission = False
        if hasattr(request.user, "account"):
            if request.user.account.active:
                has_permission = True

        return has_permission


class DataTypeAvailable(BasePermission):
    message = "This data type is not available for your account"

    def has_permission(self, request, view) -> bool:
        has_permission = False
        if hasattr(request.user, "account"):
            data_type = request.path.split("/")[2]
            if data_type in request.user.account.allowed_data_types():
                has_permission = True

        return has_permission


class RequestLimitPermission(BasePermission):
    message = "Your request limit has been exceeded"

    def has_permission(self, request, view) -> bool:
        has_permission = False
        if hasattr(request.user, "account"):
            account = request.user.account
            if all(
                [
                    account.check_daily_access(),
                    account.check_monthly_access(),
                    account.check_total_access(),
                ]
            ):
                has_permission = True

        return has_permission
