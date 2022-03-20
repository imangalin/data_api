from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
    path('buildings', views.BuildingList.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
