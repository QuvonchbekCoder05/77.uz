from rest_framework import serializers
from .models import Category, SubCategory, Ad, AdExtraInfo, SearchTerm

class SubCategorySerializer(serializers.ModelSerializer):
    # Subkategoriya ma'lumotlarini serializer orqali ko'rsatadigan qismi
    class Meta:
        model = SubCategory
        fields = ['id', 'name']

class CategorySerializer(serializers.ModelSerializer):
    # Kategoriyaga bog'langan subkategoriya ma'lumotlarini ko'rsatadigan qismi
    childs = SubCategorySerializer(many=True, source='subcategories')

    class Meta:
        model = Category
        fields = ['id', 'name', 'ads_count', 'icon', 'childs']

class AdExtraInfoSerializer(serializers.ModelSerializer):
    # Qo'shimcha e'lon ma'lumotlarini serializer orqali ko'rsatadigan qismi
    class Meta:
        model = AdExtraInfo
        fields = ['is_mine', 'status', 'expires_at']

class AdSerializer(serializers.ModelSerializer):
    # E'lonlar haqida batafsil ma'lumot olish uchun
    sub_category = SubCategorySerializer()
    extra = AdExtraInfoSerializer()
    seller = serializers.SerializerMethodField()

    class Meta:
        model = Ad
        fields = ['id', 'name', 'slug', 'sub_category', 'price', 'currency', 'published_at', 'description', 'phone_number', 'address', 'seller', 'extra', 'photos']

    def get_seller(self, obj):
        # Sotuvchi ma'lumotlarini olish uchun yordamchi funksiya yaratib oldim 
        return {
            "id": obj.seller.id,
            "full_name": obj.seller.get_full_name(),
            "profile_photo": obj.seller.profile_photo.url if obj.seller.profile_photo else None
        }

class PopularSearchTermSerializer(serializers.ModelSerializer):
    # Eng mashhur qidiruv terminlarini ko'rsatish uchun serializer yartaib oldim
    class Meta:
        model = SearchTerm
        fields = ['term']
