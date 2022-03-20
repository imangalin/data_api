from django.contrib import admin
from .models import CarTraffic

class CarTrafficAdmin(admin.ModelAdmin):
    list_display = ('geom', 'traf_day', 'shape_leng', 'region')
    search_fields = ('region', )

admin.site.register(CarTraffic, CarTrafficAdmin)
