from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.shortcuts import get_object_or_404
from django.utils import timezone
from .models import Category, Ad, SearchTerm
from .serializers import (
    CategorySerializer, AdSerializer, PopularSearchTermSerializer, AdExtraInfoSerializer
)

class PopularSearchTermsAPIView(APIView):
    # Bu APIView eng mashhur qidiruv terminlarini olish uchun xizmat qiladigan views qismi
    permission_classes = [AllowAny]  # Barcha foydalanuvchilarga kirishga ruxsat beradigan qildim

    def get(self, request):
        # 10 ta eng ko'p qidirilgan terminlarni `count` bo'yicha tartiblash uchun logika qismi
        popular_terms = SearchTerm.objects.order_by('-count')[:10]
        serializer = PopularSearchTermSerializer(popular_terms, many=True)
        # Faqat qidiruv terminlarini qaytaradi sorov jonatganda 
        return Response([term['term'] for term in serializer.data])

class AutocompleteSearchTermsAPIView(APIView):
    # Qidiruvni avtoto'ldirish uchun view qismi
    permission_classes = [AllowAny] 

    def get(self, request):
        query = request.query_params.get('q', '')  # Qidiruv so'zini olish uchun querydan foydqalamdim
        if query:
            # Qidiruv terminini yozib borish yoki count ni oshirish uchun logikasini stackOwerflofdan oldim
            search_term, created = SearchTerm.objects.get_or_create(term=query)
            if not created:
               
                search_term.count = F('count') + 1
                search_term.save(update_fields=['count'])

            # 5 ta qidiruv moslikni tartiblash uchun logika 
            terms = SearchTerm.objects.filter(term__icontains=query).order_by('-count')[:5]
        else:
            # Hech qanday qidiruv sorovi  jonatilamsa, bo'sh queryset qaytaradigan qildim
            terms = SearchTerm.objects.none()

        serializer = PopularSearchTermSerializer(terms, many=True)
        # Faqat terminlarni qaytaradi bunda ham 
        return Response([term['term'] for term in serializer.data])

class CategoriesWithChildsAPIView(generics.ListAPIView):
    # Kategoriyalarni subkategoriyalari bilan birga olish uchun views qismi
    queryset = Category.objects.prefetch_related('subcategories')
    serializer_class = CategorySerializer
    permission_classes = [AllowAny]  

class AdListAPIView(generics.ListCreateAPIView):
    # E'lonlar ro'yxatini olish va yangi e'lon yaratish uchun views
    permission_classes = [AllowAny]  
    serializer_class = AdSerializer

    def get_queryset(self):
        # Faqat "active" statusidagi e'lonlarni filterlash uchun qildim
        queryset = Ad.objects.filter(extra__status="active")
        search = self.request.query_params.get('search')  # Qidiruv so'zini oldim
        if search:
            # E'lonlarni nom bo'yicha qidiriadigan qildim
            queryset = queryset.filter(name__icontains=search)
        return queryset

class AdDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    # E'lon haqida  ma'lumot, yangilash, va o'chirish uchun views qismi
    permission_classes = [IsAuthenticated]  # Faqat tasdiqlangan foydalanuvchilar uchun kiradigan qildim yani otp tasdiq;lsansa va foydlanucch bazafa saqlansagina 
    queryset = Ad.objects.all()
    serializer_class = AdSerializer
    lookup_field = "slug"  # E'lonni slug orqali oldim

    def delete(self, request, slug):
        # E'lonni o'chirish funksiyasi logikasi
        ad = get_object_or_404(Ad, slug=slug, seller=request.user)
        ad.delete()  # Foydalanuvchi yaratgan e'lonni o'chirish logikASI
        return Response({"message": "Ad deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

    def patch(self, request, slug):
        # E'lonni qisman yangilash logikasi
        ad = get_object_or_404(Ad, slug=slug, seller=request.user)
        serializer = AdSerializer(ad, data=request.data, partial=True)  # Qisman yangilash uchun `partial=True`
        if serializer.is_valid():
            serializer.save()  # E'lonni yangilash qismi
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class MyAdsListAPIView(generics.ListAPIView):
    # Foydalanuvchining o'ziga tegishli e'lonlarni olish uchun view qismi
    permission_classes = [IsAuthenticated]  
    serializer_class = AdSerializer

    def get_queryset(self):
        # Foydalanuvchining o'z e'lonlarini filtrlash orqali oladigan qildim
        return Ad.objects.filter(seller=self.request.user)
