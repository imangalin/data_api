from django.db.models import Sum, Avg, Min, Max

from .models import CarTraffic, PedTraffic, Building


FUNCTION = {
    'sum': Sum,
    'avg': Avg,
    'min': Min,
    'max': Max
}


def apply_function(queryset, param_func, model):
    func = FUNCTION.get(param_func)
    if model == Building:
        qs = queryset.aggregate(func('storey'), func('household'), func('people'))
    else:
        qs = queryset.aggregate(func('id'), func('traf_day'))
    return qs
