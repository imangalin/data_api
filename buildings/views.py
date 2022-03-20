from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Building
from .serializers import BuildingSerializer


class BuildingList(APIView):
    def get(self, request, format=None):
        buildings = Building.objects.all()[:15]
        serializer = BuildingSerializer(buildings, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = BuildingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
