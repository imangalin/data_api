from rest_framework.routers import DefaultRouter


from api.views import PedTrafficListViewSet


router = DefaultRouter()
router.register("pedestrian", PedTrafficListViewSet, 'pedtraffic')