from rest_framework.viewsets import ReadOnlyModelViewSet
from .models import PedTraffic
from .serializers import PedTrafficSerializer


class PedTrafficListViewSet(ReadOnlyModelViewSet):
    serializer_class = PedTrafficSerializer
    queryset = PedTraffic.objects.all()[:15]
    filterset_fields = ['traf_day', ]
