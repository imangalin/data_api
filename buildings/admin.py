from django.contrib import admin
from .models import Building


@admin.register(Building)
class BuildingsAdmin(admin.ModelAdmin):
    list_display = ('geom', 'storey', 'household', 'people', 'year', 'region')
    search_fields = ('region', )


