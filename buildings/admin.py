from django.contrib import admin
from .models import Building

class BuildingsAdmin(admin.ModelAdmin):
    list_display = ('geom', 'storey', 'household', 'people', 'year', 'region')
    search_fields = ('region', )

admin.site.register(Building, BuildingsAdmin)

