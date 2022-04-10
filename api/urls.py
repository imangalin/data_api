from django.urls import include, path

from .views import BuildingListView, CarTrafficListView

urlpatterns = [
    path('buildings', BuildingListView.as_view()),
    path('cars', CarTrafficListView.as_view()),
]
