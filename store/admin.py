

from django.contrib import admin
from .models import Category, SubCategory, Ad, AdExtraInfo, SearchTerm

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'ads_count')

@admin.register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'category', 'ads_count')

@admin.register(Ad)
class AdAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'sub_category', 'price', 'currency', 'seller', 'published_at')

@admin.register(AdExtraInfo)
class AdExtraInfoAdmin(admin.ModelAdmin):
    list_display = ('is_mine', 'status', 'expires_at')

@admin.register(SearchTerm)
class SearchTermAdmin(admin.ModelAdmin):
    list_display = ('term', 'count')
