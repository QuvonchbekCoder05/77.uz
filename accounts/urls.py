

from django.urls import path
from .views import RegisterSellerView, VerifyOtpView, LoginView, UserProfileAPIView

urlpatterns = [
    path('seller/registration/', RegisterSellerView.as_view(), name='register_seller'),
    path('verify-otp/', VerifyOtpView.as_view(), name='verify_otp'),
    path('login/', LoginView.as_view(), name='login'),
    path('me/', UserProfileAPIView.as_view(), name='user_profile'),
]
