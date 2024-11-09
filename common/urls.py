

from django.urls import path
from .views import RegionListWithDistrictsAPIView, PageDetailAPIView

urlpatterns = [
    path('regions-with-districts/', RegionListWithDistrictsAPIView.as_view(), name='regions_with_districts'),
    path('pages/<slug:slug>/', PageDetailAPIView.as_view(), name='page_detail'),
]
