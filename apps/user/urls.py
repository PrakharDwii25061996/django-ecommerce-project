from django.urls import path
from . import views
from rest_framework_simplejwt.views import (
    TokenRefreshView,
    TokenVerifyView
)

urlpatterns = [
    path('user/', views.UserCreateAPIView.as_view(), name='user'),
    path('login/', views.LoginAPIView.as_view(), name='token_obtain'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('forgot/password/', views.ForgotPasswordAPIView.as_view(), name='forgot_password'),
    path('change/password/', views.ChangePasswordAPIView.as_view(), name='change_password'),
    path('edit/user/<int:pk>/', views.ProfileEditAPIView.as_view(), name='edit_profile')
]
