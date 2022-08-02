import h3
from django.core.serializers import serialize
from django.http import HttpResponse

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from rest_framework.permissions import IsAuthenticated

from .models import Building, CarTraffic, PedTraffic
from .serializers import BuildingSerializer, CarTrafficSerializer, PedTrafficSerializer
from .permissions import DataTypeAvailable, IsExpired, RequestLimitPermission

sample = [[[37.5801633155772, 55.69509046910217], [37.609946564478534, 55.690156019473264],
           [37.610032395167, 55.69001087917344], [37.61037571792091, 55.688559446542115],
           [37.61054737929786, 55.680865954062284], [37.609174088282245, 55.668524173651114],
           [37.609174088282245, 55.66813691754793], [37.59509785537211, 55.66799169552118],
           [37.56042225722762, 55.66905664453535], [37.558276490015714, 55.66949229714223],
           [37.55587323073837, 55.677091234555526], [37.55364163283799, 55.69030115923433],
           [37.55389912490341, 55.690736575284845], [37.56325466994735, 55.69223630456579],
           [37.57913334731549, 55.69480022459942], [37.5801633155772, 55.69509046910217]]]

sample2 = [[[37.510414123535156, 55.66345035345], [37.65735626220703, 55.637686135397544],
            [37.60345458984374, 55.713380738067336], [37.510414123535156, 55.66345035345]]]


def to_h3(polygon):
    poly_dict = {
        "type": "Polygon",
        "coordinates": polygon
    }
    return h3.polyfill(poly_dict, 12, geo_json_conformant=True)


class BuildingListView(APIView):
    # permission_classes = [IsAuthenticated, DataTypeAvailable, IsExpired, ]

    def get(self, request, format=None):
        self.request.user.account.request_total_count += 1
        self.request.user.account.save()
        buildings = Building.objects.all()[:5]
        serializer = BuildingSerializer(buildings, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):

        buildings = Building.objects.filter(h3_12__in=to_h3(sample2))[:5]

        return HttpResponse(serialize('geojson', buildings,
                                      geometry_field='geom',
                                      fields=('id', 'storey', 'household', 'year', 'people')))


class CarTrafficListView(APIView):
    # permission_classes = [IsAuthenticated, DataTypeAvailable, IsExpired, RequestLimitPermission, ]

    def get(self, request, format=None):
        account = self.request.user.account
        account.request_total_count += 1
        account.save()
        buildings = CarTraffic.objects.all()[:account.limit_data_size]
        serializer = CarTrafficSerializer(buildings, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):

        car_traffic = CarTraffic.objects.filter(h3_12__in=to_h3(sample2))[:5]

        return HttpResponse(serialize('geojson', car_traffic,
                                      geometry_field='geom',
                                      fields=('id', 'traffic_total')))


# class PedTrafficListViewSet(ReadOnlyModelViewSet):
#     permission_classes = [IsAuthenticated, DataTypeAvailable, IsExpired, ]
#     serializer_class = PedTrafficSerializer
#     queryset = PedTraffic.objects.all()[:15]
#     filterset_fields = ['traf_day', ]


class PedTrafficListView(APIView):
    # permission_classes = [IsAuthenticated, DataTypeAvailable, IsExpired, RequestLimitPermission, ]

    def get(self, request, format=None):
        account = self.request.user.account
        account.request_total_count += 1
        account.save()
        buildings = CarTraffic.objects.all()[:account.limit_data_size]
        serializer = CarTrafficSerializer(buildings, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):

        ped_traffic = PedTraffic.objects.filter(h3_12__in=to_h3(sample2))[:5]

        return HttpResponse(serialize('geojson', ped_traffic,
                                      geometry_field='geom',
                                      fields=('id', 'traffic_total')))
