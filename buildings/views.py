from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Building
# from .serializers import BuildingSerializer
from django.http import HttpResponse
from django.core.serializers import serialize
# from my_app.models import City




class BuildingList(APIView):
    def get(self, request, format=None):
        buildings = Building.objects.all()[:20]
        # serializer = BuildingSerializer(buildings, many=True)
        # return Response(serializer.data)
        return HttpResponse(serialize('geojson', buildings,
          geometry_field='geom',
          fields=('id', 'storey', 'household')))

    # def post(self, request, format=None):
    #     serializer = BuildingSerializer(data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
