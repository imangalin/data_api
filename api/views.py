import json

from django.contrib.gis.geos import Polygon
from django.db.models import Sum, Avg

from django.http import HttpResponse, JsonResponse
from django.core.serializers import serialize
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.permissions import IsAuthenticated

from .models import Building, CarTraffic, PedTraffic
from .serializers import BuildingSerializer, CarTrafficSerializer, PedTrafficSerializer
from .permissions import DataTypeAvailable, IsExpired, RequestLimitPermission
from .utils import apply_function


# class BuildingListView(APIView):
#     permission_classes = [IsAuthenticated, DataTypeAvailable, IsExpired, ]
#
#     def get(self, request, format=None):
#         account = self.request.user.account
#         account.request_total_count += 1
#         account.request_day_count += 1
#         account.save()
#         buildings = Building.objects.all()[:20]
#         serializer = BuildingSerializer(buildings, many=True)
#         return Response(serializer.data)
#
#     def post(self, request, format=None):
#         serializer = BuildingSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class CarTrafficListView(APIView):
#     permission_classes = [IsAuthenticated, DataTypeAvailable, IsExpired, RequestLimitPermission, ]
#
#     def get(self, request, format=None):
#         account = self.request.user.account
#         account.request_total_count += 1
#         account.request_day_count += 1
#         account.save()
#         buildings = CarTraffic.objects.all()[:account.limit_data_size]
#         serializer = CarTrafficSerializer(buildings, many=True)
#         return Response(serializer.data)
#
#     def post(self, request, format=None):
#         serializer = CarTrafficSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PedTrafficListViewSet(ReadOnlyModelViewSet):
    permission_classes = [IsAuthenticated, DataTypeAvailable, IsExpired, ]
    serializer_class = PedTrafficSerializer
    queryset = PedTraffic.objects.all()[:15]
    filterset_fields = ['traf_day', ]


class BuildingListView(APIView):

    def post(self, request, format=None):
        buildings = Building.objects.all()

        sample = (((37.5801633155772,55.69509046910217),(37.609946564478534,55.690156019473264),(37.610032395167,55.69001087917344),(37.61037571792091,55.688559446542115),(37.61054737929786,55.680865954062284),(37.609174088282245,55.668524173651114),(37.609174088282245,55.66813691754793),(37.59509785537211,55.66799169552118),(37.56042225722762,55.66905664453535),(37.558276490015714,55.66949229714223),(37.55587323073837,55.677091234555526),(37.55364163283799,55.69030115923433),(37.55389912490341,55.690736575284845),(37.56325466994735,55.69223630456579),(37.57913334731549,55.69480022459942),(37.5801633155772,55.69509046910217)))
        sample_polygon = Polygon(sample, srid=4326)
        print(type(sample_polygon))
        print(buildings.first().geom)

        qs = buildings.filter(geom__within=sample_polygon)
        return HttpResponse(serialize('geojson', qs,
                                      geometry_field='geom',
                                      fields=('id', 'traf_day', 'region')))
        return Response('Не вышло', status=status.HTTP_400_BAD_REQUEST)

class CarTrafficListView(APIView):
    # queryset = CarTraffic.objects.all()

    def get(self, request, format=None):
        carTraffic = CarTraffic.objects.all()[:5]
        param_func = self.request.query_params.get('func')
        param_order = self.request.query_params.get('orderBy')
        if param_func:
            carTraffic = apply_function(carTraffic, param_func, CarTraffic)
            #update({'polygon': request.get('polygon')})
            #добавить исходный полигон из запроса

            return JsonResponse(carTraffic, safe=False)
                    #{'id__sum': 15, 'traf_day__sum': 11235}

        if param_order:
          carTraffic = carTraffic.filter(traf_day__gte=130000).order_by(param_order)

        return HttpResponse(serialize('geojson', carTraffic,
          geometry_field='geom',
          fields=('id', 'traf_day', 'region')))

# добавить полигон и точку (к ней строится буфер)
#в дальнейшем мультиполигон в запросе

    def post(self, request, format=None):
        carTraffic = CarTraffic.objects.all()
        print(request.data.get('polygon'))

        sample = (((37.5801633155772,55.69509046910217),(37.609946564478534,55.690156019473264),(37.610032395167,55.69001087917344),(37.61037571792091,55.688559446542115),(37.61054737929786,55.680865954062284),(37.609174088282245,55.668524173651114),(37.609174088282245,55.66813691754793),(37.59509785537211,55.66799169552118),(37.56042225722762,55.66905664453535),(37.558276490015714,55.66949229714223),(37.55587323073837,55.677091234555526),(37.55364163283799,55.69030115923433),(37.55389912490341,55.690736575284845),(37.56325466994735,55.69223630456579),(37.57913334731549,55.69480022459942),(37.5801633155772,55.69509046910217)))
        sample2 = (((55.69509046910217,37.5801633155772),(55.690156019473264,37.609946564478534),( 55.66813691754793,37.609174088282245),( 55.66799169552118,37.59509785537211),( 55.66905664453535,37.56042225722762),( 55.66949229714223,37.558276490015714),( 55.69480022459942,37.57913334731549),( 55.69509046910217,37.5801633155772)))
        sample_polygon = Polygon(sample2, srid=4326)

        qs = carTraffic.filter(geom__in=sample_polygon)
        return HttpResponse(serialize('geojson', qs,
                                      geometry_field='geom',
                                      fields=('id', 'traf_day', 'region')))
        return Response('Не вышло', status=status.HTTP_400_BAD_REQUEST)


# [[[37.5801633155772,55.69509046910217],[37.609946564478534,55.690156019473264],[37.610032395167,55.69001087917344],[37.61037571792091,55.688559446542115],[37.61054737929786,55.680865954062284],[37.609174088282245,55.668524173651114],[37.609174088282245,55.66813691754793],[37.59509785537211,55.66799169552118],[37.56042225722762,55.66905664453535],[37.558276490015714,55.66949229714223],[37.55587323073837,55.677091234555526],[37.55364163283799,55.69030115923433],[37.55389912490341,55.690736575284845],[37.56325466994735,55.69223630456579],[37.57913334731549,55.69480022459942],[37.5801633155772,55.69509046910217]]]

# (((37.5801633155772,55.69509046910217),(37.609946564478534,55.690156019473264),(37.610032395167,55.69001087917344),(37.61037571792091,55.688559446542115),(37.61054737929786,55.680865954062284),(37.609174088282245,55.668524173651114),(37.609174088282245,55.66813691754793),(37.59509785537211,55.66799169552118),(37.56042225722762,55.66905664453535),(37.558276490015714,55.66949229714223),(37.55587323073837,55.677091234555526),(37.55364163283799,55.69030115923433),(37.55389912490341,55.690736575284845),(37.56325466994735,55.69223630456579),(37.57913334731549,55.69480022459942),(37.5801633155772,55.69509046910217)))