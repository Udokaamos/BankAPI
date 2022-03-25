from django.urls import path
from . import views

from rest_framework_simplejwt.views import (
   TokenObtainPairView,
   TokenRefreshView,
)

urlpatterns = [
    path('users/', views.user_view, name="users"),
    path('users/signup', views.signup_view, name="signup"),
    path('auth/', views.login_view, name="login"),
    path('users/update/<int:user_id>/', views.update_view, name="update"),
    path('token/', TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path('token/refresh/', TokenRefreshView.as_view(), name="token_refresh"),
    
    
    
]