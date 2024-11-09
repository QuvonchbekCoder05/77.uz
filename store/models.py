from django.db import models
from django.utils.text import slugify
from django.contrib.auth import get_user_model
from django.utils import timezone

# Foydalanuvchi modelini olish uchun Django ichidagi `get_user_model` funksiyasidan foydalanamiz.
User = get_user_model()

class Category(models.Model):
    # Kategoriya nomini saqlaydigan model
    name = models.CharField(max_length=255)
    # E'lonlar sonini saqlaydi
    ads_count = models.IntegerField(default=0)
    # Kategoriya uchun ikonka rasmini saqlaydi
    icon = models.ImageField(upload_to='category_icons/', blank=True, null=True)

    def __str__(self):
       
        return self.name

class SubCategory(models.Model):
    # Subkategoriya nomini saqlaydi
    name = models.CharField(max_length=255)
    # Category kategoriya bilan bog'lanadigan qildim 
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='subcategories')
    # Subkategoriyadagi e'lonlar sonini saqlaydigan model yaratdim
    ads_count = models.IntegerField(default=0)

    def __str__(self):
        return self.name

class AdExtraInfo(models.Model):
    # E'lon egasi ekanligini belgilaydigan qilib qoydim
    is_mine = models.BooleanField(default=False)
    # E'lon holatini saqlaydi (active yoki expired)
    status = models.CharField(max_length=50, choices=[('active', 'Active'), ('expired', 'Expired')])
    # E'lonning tugash sanasi uchun models yartadim
    expires_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Status: {self.status}, Expires at: {self.expires_at}"

class Ad(models.Model):
    
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True, max_length=255)
    # Subkategoriya bilan bog'lanadigan qilib qildim 
    sub_category = models.ForeignKey(SubCategory, on_delete=models.CASCADE, related_name='ads')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=10)
    published_at = models.DateTimeField(auto_now_add=True)
    description = models.TextField(blank=True)
    phone_number = models.CharField(max_length=20)
    address = models.CharField(max_length=255)
    # Sotuvchi bilan bog'lanadgan qildim
    seller = models.ForeignKey(User, on_delete=models.CASCADE)
    # Qo'shimcha ma'lumotlar bilan bog'lanadigan qildim
    extra = models.OneToOneField(AdExtraInfo, on_delete=models.CASCADE, related_name='ad')
    # E'lon uchun rasm yuklanadigan qildim
    photos = models.ImageField(upload_to='ad_photos/', blank=True, null=True)

    def save(self, *args, **kwargs):
        # Agar slug yo'q bo'lsa, nomidan avtomatik ravishda slug hosil qiladigan qilib qoydim
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class SearchTerm(models.Model):
    # Qidiruv uchun terminni saqlaydigan qildim
    term = models.CharField(max_length=255, unique=True)
    # Qidiruv soniini saqlaydad
    count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.term
