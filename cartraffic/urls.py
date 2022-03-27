from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from .views import CarTrafficList

urlpatterns = [
    path('', CarTrafficList.as_view(), name='cartraffic'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
