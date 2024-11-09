

from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from django.shortcuts import get_object_or_404
from .models import Region, Page
from .serializers import RegionSerializer, PageSerializer

class RegionListWithDistrictsAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        regions = Region.objects.prefetch_related('districts').all()
        serializer = RegionSerializer(regions, many=True)
        return Response(serializer.data)

class PageDetailAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, slug):
        page = get_object_or_404(Page, slug=slug)
        serializer = PageSerializer(page)
        return Response(serializer.data)
