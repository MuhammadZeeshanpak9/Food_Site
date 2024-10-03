from django.contrib import admin
from django.urls import path
from .views import UserReg,AdminLoginView,UserProfileView,ChangePasswordView,RequestPasswordResetView,SetNewPasswordView

urlpatterns = [
    path('Reg/', UserReg.as_view(), name='user-register'),
    path('login/', AdminLoginView.as_view(), name='user-login'),
    path('profile/', UserProfileView.as_view(), name='user-profile'),
    path('changepass/', ChangePasswordView.as_view(), name='change-password'),
    path('password-reset/', RequestPasswordResetView.as_view(), name="password-reset"),
     path('password-reset-confirm/<uidb64>/<token>/', SetNewPasswordView.as_view(), name='password-reset-confirm'),
]
