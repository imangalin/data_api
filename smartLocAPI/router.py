from rest_framework.routers import DefaultRouter


from pedtraffic.views import PedTrafficListViewSet


router = DefaultRouter()
router.register("pedestrian", PedTrafficListViewSet, 'pedtraffic')