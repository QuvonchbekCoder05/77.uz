

from rest_framework import serializers
from .models import Region, District, Page

class DistrictSerializer(serializers.ModelSerializer):
    class Meta:
        model = District
        fields = ['id', 'name']

class RegionSerializer(serializers.ModelSerializer):
    districts = DistrictSerializer(many=True)

    class Meta:
        model = Region
        fields = ['id', 'name', 'districts']

class PageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Page
        fields = ['slug', 'content']
