from django.urls import path
from . import views

from rest_framework_simplejwt.views import (
   TokenObtainPairView,
   TokenRefreshView,
)

urlpatterns = [
    path('users/', views.user_view, name="users"),
    path('users/signup', views.signup_view, name="signup"),
    path('users/login/', views.login_view, name="login"),
    path('users/generate_acc_num/', views.generate_acc_num, name="genrate_acc_num"),
    path('token/', TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path('token/refresh/', TokenRefreshView.as_view(), name="token_refresh"),
    
    
    
]