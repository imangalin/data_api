from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import CarTraffic
from .serializers import CarTrafficSerializer


class CarTrafficList(APIView):
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
