from datetime import date

from rest_framework.permissions import BasePermission


class IsExpired(BasePermission):
    message = 'Your account has been expired'

    def has_permission(self, request, view):
        has_permission = False
        if hasattr(request.user, 'account'):
            if request.user.account.access_expiration >= date.today():
                has_permission = True

        return has_permission


class DataTypeAvailable(BasePermission):
    message = 'This data type is not available for your account'

    def has_permission(self, request, view):
        has_permission = False
        if hasattr(request.user, 'account'):
            data_type = request.path.split('/')[2]
            if data_type in request.user.account.data_type.values_list('slug', flat=True):
                has_permission = True

        return has_permission


class RequestLimitPermission(BasePermission):
    message = 'Your request limit has been exceeded'

    def has_permission(self, request, view):
        has_permission = False
        if hasattr(request.user, 'account'):
            account = request.user.account
            if (
                account.request_day_count <= account.request_day_limit
                & account.request_total_count <= account.request_total_limit
            ):
                has_permission = True

        return has_permission
