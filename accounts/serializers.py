# serializers.py
from rest_framework import serializers
from .models import CustomUser, Seller

# Foydalanuvchi ro'yxatga olish uchun serializer
class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)  # Parol faqat yozish uchun qilib qoyamiz 
    project_name = serializers.CharField(write_only=True)  
    category_id = serializers.IntegerField(write_only=True)  
    seller_address = serializers.CharField(write_only=True) 

    class Meta:
        model = CustomUser  # Modelni belgilaymiz 
        fields = ['full_name', 'email', 'password', 'phone_number', 'address', 'project_name', 'category_id', 'seller_address']  # Maydonlar

    # Foydalanuvchi yaratish
    def create(self, validated_data):
        user = CustomUser(
            email=validated_data['email'],  # Emailni saqlaymiz 
            full_name=validated_data['full_name'],  
            phone_number=validated_data.get('phone_number', ''), 
            address=validated_data.get('address', ''), 
        )
        user.set_password(validated_data['password']) 
        user.generate_otp()  # OTP generatsiya qilamiz
        user.save()  # Foydalanuvchini saqlaymiz

        # Sotuvchi yaratish
        Seller.objects.create(
            user=user,  # Foydalanuvchini ulab qoyamiz
            project_name=validated_data['project_name'],  
            category_id=validated_data.get('category_id'),  
            address=validated_data['seller_address'] 
        )

        return user  # Foydalanuvchini qaytaramiz 

# OTP tasdiqlash uchun serializer
class VerifyOtpSerializer(serializers.Serializer):
    email = serializers.EmailField()  # Foydalanuvchi emaili
    otp = serializers.CharField(max_length=6)  # OTP maydoni

# Foydalanuvchi login uchun serializer yartamiz
class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()  # Foydalanuvchi emaili
    password = serializers.CharField(write_only=True)  # Parol

# Foydalanuvchi profilini ko'rsatish uchun serializer
class UserProfileSerializer(serializers.ModelSerializer):
    address = serializers.SerializerMethodField()  # Manzilni formatlash

    class Meta:
        model = CustomUser
        fields = ['id', 'full_name', 'email', 'phone_number', 'profile_photo', 'address']

    # Manzilni formallashtirish logikasini yozilgan qismi
    def get_address(self, obj):
        return {
            "name": obj.address,  # Manzil
            "lat": obj.lat,  # Kenglik
            "long": obj.long  # Uzunlik
        }
