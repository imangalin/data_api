from django.urls import include, path

from .views import BuildingListView, CarTrafficListView, PedTrafficListView

urlpatterns = [
    path('buildings/', BuildingListView.as_view()),
    path('cars/', CarTrafficListView.as_view()),
    path('pedestrian/', PedTrafficListView.as_view()),
]
