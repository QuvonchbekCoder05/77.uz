from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth import authenticate
from .models import CustomUser
from .serializers import (
    UserRegistrationSerializer,
    VerifyOtpSerializer,
    UserLoginSerializer,
    UserProfileSerializer
)

# Ro'yxatdan o'tish uchun view
class RegisterSellerView(APIView):
    permission_classes = [AllowAny]  # Har qanday foydalanuvchi kirishi mumkin

    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)  # Foydalanuvchi ro'yxatdan o'tishi uchun serializerni yaratib oldim
        if serializer.is_valid():
            user = serializer.save()  # Agar ma'lumotlar to'g'ri bo'lsa, foydalanuvchini saqlayman
            # E-pochtaga OTP kodini yuboradigan qismi
            send_mail(
                'Your OTP Code',  # Xabar mavzusi
                f'Your OTP code is {user.otp}',  # Xabar matni, OTP bilan
                settings.EMAIL_HOST_USER,  # Jo'natuvchi email
                [user.email],  # Qabul qiluvchi email
                fail_silently=False  # Xato yuz bersa, xabarni chiqaradi
            )
            return Response({"message": "OTP sent to your email."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  # Agar xato bo'lsa, xatolikni qaytaradigan qildim

# OTP ni tasdiqlash uchun view
class VerifyOtpView(APIView):
    permission_classes = [AllowAny]  # Har qanday foydalanuvchi kirishi mumkin bunga ham

    def post(self, request):
        serializer = VerifyOtpSerializer(data=request.data)  # OTPni tekshirish uchun serializer yaratib oldim
        if serializer.is_valid():
            email = serializer.validated_data['email']  # Foydalanuvchi emailini oldim
            otp = serializer.validated_data['otp']  # Foydalanuvchi kiritgan OTPni oldim
            try:
                user = CustomUser.objects.get(email=email, otp=otp)  # Email va OTP bo'yicha foydalanuvchini topib olaman
                user.is_verified = True  # Foydalanuvchini tasdiqlangan deb belgilayman
                user.save()  # O'zgarishlarni saqlayman
                return Response({"message": "Account verified successfully."}, status=status.HTTP_200_OK)
            except CustomUser.DoesNotExist:
                return Response({"error": "Invalid OTP or email."}, status=status.HTTP_400_BAD_REQUEST)  # Agar foydalanuvchi topilmasa, xatolikni qaytaradi
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Foydalanuvchini tizimga kiritish (login) uchun view
class LoginView(APIView):
    permission_classes = [AllowAny] 
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)  # Login uchun serializerni yaratdim
        if serializer.is_valid():
            email = serializer.validated_data['email']  # Foydalanuvchi emailini oldim
            password = serializer.validated_data['password']  # Foydalanuvchi parolini oldim
            user = authenticate(request, email=email, password=password)  # Foydalanuvchini autentifikatsiya qidim
            if user and user.is_verified:
                refresh = RefreshToken.for_user(user)  # Tasdiqlangan foydalanuvchi uchun JWT token generatsiya qidim
                return Response({
                    'access_token': str(refresh.access_token),  # Kirish tokenini yubordim
                    'refresh_token': str(refresh)  # Yangilash tokenini yubordim
                }, status=status.HTTP_200_OK)
            return Response({"error": "Noto'g'ri ma'lumotlar yoki tasdiqlanmagan hisob."}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Foydalanuvchi profilini olish uchun API
class UserProfileAPIView(APIView):
    permission_classes = [IsAuthenticated]  # Tasdiqlangan foydalanuvchilar uchun ruxsat faqat

    def get(self, request):
        serializer = UserProfileSerializer(request.user)  # Foydalanuvchining profilini olish uchun serializer chaqirdim
        return Response(serializer.data)  # Profil ma'lumotlarini qaytaraman 
