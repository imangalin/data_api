import json
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import CarTraffic
from .serializers import CarTrafficSerializer
from rest_framework import generics

from django.db.models import Sum, Avg

from django.http import HttpResponse, JsonResponse
from django.core.serializers import serialize


class CarTrafficList(APIView):
    def get(self, request, format=None):
        carTraffic = CarTraffic.objects.all()
        param_func = self.request.query_params.get('func')
        param_order = self.request.query_params.get('orderBy')
        if param_func:
          if param_func == "avg":
            carTraffic = carTraffic.aggregate(Sum('id'), Sum('traf_day'))
        if param_order:
          carTraffic = CarTraffic.objects.filter(traf_day__gte = 130000).order_by(param_order)[:3]

        serializer = CarTrafficSerializer(carTraffic, many=True)
        # return Response(serializer.data)

        # return HttpResponse(serialize('json', carTraffic))
        carTraffic_list = list(carTraffic)
        # return JsonResponse(serialize('json', carTraffic), safe=False)

        # qr = CarTraffic.objects.all().values()[:5]
        # qr_json = json.dumps(list(qr), ensure_ascii=False, default=str)
        # return JsonResponse(qr_json, safe=False)

        return HttpResponse(serialize('geojson', carTraffic,
          geometry_field='geom',
          fields=('id', 'traf_day', 'region')))

    def post(self, request, format=None):
        serializer = CarTrafficSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
