from datetime import date

from rest_framework.permissions import BasePermission


class IsExpired(BasePermission):
    def has_permission(self, request, view):
        has_permission = False
        if hasattr(request.user, 'account'):
            if request.user.account.access_expiration >= date.today():
                has_permission = True

        return has_permission


class RegionAvailable(BasePermission):
    def has_permission(self, request, view):
        has_permission = False
        if hasattr(request.user, 'account'):
            #нужен модуль для проверки вхождения координат из GET в account.region
            #план: в регионе храним полигон с его границами, сперва проверяем, входит ли полигон из GET в эти границы,
            #затем отправляем запрос на данные
            pass


class DataTypeAvailable(BasePermission):
    def has_permission(self, request, view):
        has_permission = False
        if hasattr(request.user, 'account'):
            data_type = request.path.split('/')[2]
            if data_type in request.user.account.data_type.values_list('slug', flat=True):
                has_permission = True

        return has_permission
