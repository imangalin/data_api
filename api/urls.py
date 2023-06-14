from django.urls import path

from .views import BuildingListView, CarTrafficListView, PedTrafficListView

app_name = "api"

urlpatterns = [
    path("buildings/", BuildingListView.as_view(), name="buildings"),
    path("cars/", CarTrafficListView.as_view(), name="cars"),
    path("pedestrian/", PedTrafficListView.as_view(), name="pedestrian"),
]
