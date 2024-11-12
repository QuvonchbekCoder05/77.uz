# models.py
from django.contrib.auth.models import AbstractBaseUser,  PermissionsMixin
from django.db import models
import random
from .managers import CustomUserManager #managaerdan CustomManagerni chqirib oldim

# Foydalanuvchi modeli
class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True) 
    password = models.CharField(max_length=255)

    full_name = models.CharField(max_length=128)  
    phone_number = models.CharField(max_length=15, null=True, blank=True)  
    profile_photo = models.ImageField(upload_to='accounts/', null=True, blank=True)  
    address = models.CharField(max_length=256, null=True, blank=True)  
    lat = models.FloatField(null=True, blank=True)  
    long = models.FloatField(null=True, blank=True)
    is_active = models.BooleanField(default=True)  # Foydalanuvchi faolmi yoki yo'qmi tekshirmaiz
    is_verified = models.BooleanField(default=False)  # Foydalanuvchi tasdiqlanganmi yoki yo'qmi tekshiramiz
    otp = models.CharField(max_length=6, blank=True, null=True)  

    USERNAME_FIELD = 'email'  # Login uchun asosiy maydon
    REQUIRED_FIELDS = []  # Majburiy maydonlar yo'q deb belgilaymiz

    objects = CustomUserManager()  # Maxsus foydalanuvchi manageri beramiz

    def __str__(self):
        return self.email  # Foydalanuvchi email orqali ko'rsatiladi

    # OTP kod yaratish va saqlash qismi
    def generate_otp(self):
        self.otp = str(random.randint(100000, 999999))  # 6 xonali tasodifiy kod yarataman random orqali
        self.save()  # Saqlayman keyin

# Sotuvchi modeli
class Seller(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='seller_profile')  # CustomUser bilan bog'lanmiz
    project_name = models.CharField(max_length=128) 
    category_id = models.IntegerField(null=True, blank=True) 
    address = models.CharField(max_length=256)  # Sotuvchining manzili

    def __str__(self):
        return f"Seller: {self.project_name} (User: {self.user.email})"  # Sotuvchi ma'lumotlari
