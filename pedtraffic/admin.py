from django.contrib import admin

from .models import PedTraffic


@admin.register(PedTraffic)
class PedTrafficAdmin(admin.ModelAdmin):
    list_display = ('geom', 'traf_day')

