from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from rest_framework.viewsets import ReadOnlyModelViewSet

from .models import Building, CarTraffic, PedTraffic
from .serializers import BuildingSerializer, CarTrafficSerializer, PedTrafficSerializer
from .permissions import DataTypeAvailable, IsExpired, RequestLimitPermission


class BuildingListView(APIView):
    permission_classes = [DataTypeAvailable, IsExpired, ]

    def get(self, request, format=None):
        self.request.user.account.request_total_count += 1
        self.request.user.account.save()
        buildings = Building.objects.all()[:20]
        serializer = BuildingSerializer(buildings, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = BuildingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CarTrafficListView(APIView):
    permission_classes = [DataTypeAvailable, IsExpired, RequestLimitPermission, ]

    def get(self, request, format=None):
        account = self.request.user.account
        account.request_total_count += 1
        account.save()
        buildings = CarTraffic.objects.all()[:account.limit_data_size]
        serializer = CarTrafficSerializer(buildings, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = CarTrafficSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PedTrafficListViewSet(ReadOnlyModelViewSet):
    permission_classes = [DataTypeAvailable, IsExpired, ]
    serializer_class = PedTrafficSerializer
    queryset = PedTraffic.objects.all()[:15]
    filterset_fields = ['traf_day', ]
