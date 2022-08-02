from django.contrib import admin
from .models import Building, CarTraffic, PedTraffic


@admin.register(Building)
class BuildingsAdmin(admin.ModelAdmin):
    list_display = ('storey', 'household')
    # search_fields = ('region', )


@admin.register(CarTraffic)
class CarTrafficAdmin(admin.ModelAdmin):
    list_display = ('geom', 'traffic_total')
    # search_fields = ('region', )


@admin.register(PedTraffic)
class PedTrafficAdmin(admin.ModelAdmin):
    list_display = ('geom', 'traffic_total')
    # search_fields = ('region', )
