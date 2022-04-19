from rest_framework.routers import DefaultRouter

from .views import PedTrafficListViewSet


router = DefaultRouter()
router.register("pedestrian", PedTrafficListViewSet, 'pedtraffic')