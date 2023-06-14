import re
import h3

from django.db.models import Sum, Avg, Min, Max, QuerySet
from django.contrib.auth.models import User

from .models import Building


FUNCTION = {
    'sum': Sum,
    'avg': Avg,
    'min': Min,
    'max': Max
}


def apply_function(queryset: QuerySet, param_func: str) -> QuerySet:
    func = FUNCTION.get(param_func)
    if queryset.model == Building:
        qs = queryset.aggregate(func('storey'), func('household'), func('people'))
    else:
        qs = queryset.aggregate(func('traffic_total'))
    return qs


def to_h3_poly(polygon: list):
    poly_dict = {
        "type": "Polygon",
        "coordinates": polygon
    }
    return h3.polyfill(poly_dict, 12, geo_json_conformant=True)


def to_h3_buffer(point: str, size: int):
    coord = point.split(',')
    hex_user = h3.geo_to_h3(float(coord[1]), float(coord[0]), 12)
    dist_res = size // 18.4 + 1
    ped_zone_hex = h3.k_ring(hex_user, dist_res)
    return ped_zone_hex


def handle_bbox(param_bbox: str) -> list:
    formatted_bbox = [float(x) for x in re.split(",|~", param_bbox)]
    param_a = [formatted_bbox[0], formatted_bbox[1]]
    param_b = [formatted_bbox[2], formatted_bbox[1]]
    param_c = [formatted_bbox[2], formatted_bbox[3]]
    param_d = [formatted_bbox[0], formatted_bbox[3]]
    return [[param_a, param_b, param_c, param_d]]


def count_requests(user: User) -> None:
    user.account.request_total_count += 1
    user.account.request_day_count += 1
    user.account.request_month_count += 1
    user.account.save()
