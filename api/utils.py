import h3

from django.db.models import Sum, Avg, Min, Max

from .models import Building


FUNCTION = {
    'sum': Sum,
    'avg': Avg,
    'min': Min,
    'max': Max
}


def apply_function(queryset, param_func):
    func = FUNCTION.get(param_func)
    if queryset.model == Building:
        qs = queryset.aggregate(func('storey'), func('household'), func('people'))
    else:
        qs = queryset.aggregate(func('traffic_total'))
    return qs


def to_h3_poly(polygon):
    poly_dict = {
        "type": "Polygon",
        "coordinates": polygon
    }
    return h3.polyfill(poly_dict, 12, geo_json_conformant=True)


def to_h3_buffer(point, size):
    coord = point.split(',')
    hex_user = h3.geo_to_h3(float(coord[1]), float(coord[0]), 12)
    dist_res = size // 18.4 + 1
    ped_zone_hex = h3.k_ring(hex_user, dist_res)
    return ped_zone_hex