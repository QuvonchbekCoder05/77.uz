

from django.contrib import admin
from .models import Region, District, Page

@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')

@admin.register(District)
class DistrictAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'region')

@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    list_display = ('slug', 'content')
