from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from rest_framework.viewsets import ReadOnlyModelViewSet

from .models import Building, CarTraffic, PedTraffic
from .serializers import BuildingSerializer, CarTrafficSerializer, PedTrafficSerializer


class BuildingListView(APIView):
    def get(self, request, format=None):
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
    def get(self, request, format=None):
        buildings = CarTraffic.objects.all()[:15]
        serializer = CarTrafficSerializer(buildings, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = CarTrafficSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PedTrafficListViewSet(ReadOnlyModelViewSet):
    serializer_class = PedTrafficSerializer
    queryset = PedTraffic.objects.all()[:15]
    filterset_fields = ['traf_day', ]
