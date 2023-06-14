from django.contrib import admin
from .models import Building, CarTraffic, PedTraffic


@admin.register(Building)
class BuildingsAdmin(admin.ModelAdmin):
    list_display = ("storey", "household")


@admin.register(CarTraffic)
class CarTrafficAdmin(admin.ModelAdmin):
    list_display = ("traffic_total",)


@admin.register(PedTraffic)
class PedTrafficAdmin(admin.ModelAdmin):
    list_display = ("traffic_total",)
