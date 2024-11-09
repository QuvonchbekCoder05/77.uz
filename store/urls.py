

from django.urls import path
from .views import (
    PopularSearchTermsAPIView,
    AutocompleteSearchTermsAPIView,
    CategoriesWithChildsAPIView,
    AdListAPIView,
    AdDetailAPIView,
    MyAdsListAPIView
)

urlpatterns = [
    path('search/populars/', PopularSearchTermsAPIView.as_view(), name='popular_search_terms'),
    path('search/complete/', AutocompleteSearchTermsAPIView.as_view(), name='autocomplete_search_terms'),
    path('categories-with-childs/', CategoriesWithChildsAPIView.as_view(), name='categories_with_childs'),
    path('ads/', AdListAPIView.as_view(), name='ad_list_create'),
    path('ads/<slug:slug>/', AdDetailAPIView.as_view(), name='ad_detail'),
    path('my-ads/', MyAdsListAPIView.as_view(), name='my_ads'),
]
