from django.contrib import admin
from basic.places.models import *


class PlaceTypeAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
admin.site.register(PlaceType, PlaceTypeAdmin)


class CityAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('city', 'state')}
admin.site.register(City, CityAdmin)


class PointAdmin(admin.ModelAdmin):
    list_display = ('address', 'city', 'zip', 'latitude', 'longitude')
    list_filter = ('city',)
    search_fields = ('address',)
admin.site.register(Point, PointAdmin)


class PlaceAdmin(admin.ModelAdmin):
    list_display = ('title', 'point', 'city', 'status')
    list_filter = ('status', 'place_types')
    search_fields = ('title',)
    prepopulated_fields = {'slug': ('title',)}
admin.site.register(Place, PlaceAdmin)