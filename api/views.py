import re

from django.core.serializers import serialize
from django.http import HttpResponse, JsonResponse

from rest_framework.views import APIView
from rest_framework.parsers import JSONParser
from rest_framework.permissions import IsAuthenticated

from .models import Building, CarTraffic, PedTraffic
from .permissions import DataTypeAvailable, IsExpired, RequestLimitPermission
from .utils import apply_function, to_h3_poly, to_h3_buffer, handle_bbox, count_requests


{
    "func": "avg",
    "bbox": "37.51,55.67~37.65,55.63",
    "polygon": [
        [
            [37.510414123535156, 55.66345035345],
            [37.65735626220703, 55.637686135397544],
            [37.60345458984374, 55.713380738067336],
            [37.510414123535156, 55.66345035345],
        ]
    ],
    "point": "37.578808,55.694946",
    "size": 100,
}


class BaseListView(APIView):
    permission_classes = [
        IsAuthenticated,
        DataTypeAvailable,
        IsExpired,
        RequestLimitPermission,
    ]

    def get_queryset(self):
        pass

    def get_fields(self):
        if self.get_queryset().model == Building:
            return ("id", "storey", "household", "year", "people")
        else:
            return ("id", "traffic_total")

    def post(self, request):
        parser_classes = [JSONParser]

        count_requests(self.request.user)

        param_func = request.data.get("func", None)
        param_order = request.data.get("order", None)
        param_poly = request.data.get("polygon", None)
        param_bbox = request.data.get("bbox", None)
        param_limit = request.data.get("limit", 1000)
        param_point = request.data.get("point", None)
        param_size = request.data.get("size", None)

        if not any([param_poly, param_bbox, param_point]):
            return JsonResponse({"detail": "Please pass coordinates"}, status=400)

        if param_bbox:
            param_poly = handle_bbox(param_bbox)

        if param_point and param_size:
            ped_zone_hex = to_h3_buffer(param_point, param_size)

        polygon = to_h3_poly(param_poly) if param_poly else ped_zone_hex
        qs = self.get_queryset().filter(
            h3_12__in=polygon, region__in=self.request.user.account.region.all()
        )

        if param_func:
            func_qs = apply_function(qs, param_func)
            return JsonResponse(func_qs)

        if param_order:
            qs = qs.order_by(param_order)

        return HttpResponse(
            serialize(
                "geojson",
                qs[: int(param_limit)],
                geometry_field="geom",
                fields=self.get_fields(),
            )
        )


class BuildingListView(BaseListView):
    def get_queryset(self):
        return Building.objects.all()


class CarTrafficListView(BaseListView):
    def get_queryset(self):
        return CarTraffic.objects.all()


class PedTrafficListView(BaseListView):
    def get_queryset(self):
        return PedTraffic.objects.all()
