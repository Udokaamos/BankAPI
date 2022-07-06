from django.urls import path
from . import views

from rest_framework_simplejwt.views import (
   TokenObtainPairView,
   TokenRefreshView,
)

urlpatterns = [
    path('users/', views.user_view, name="users"),
    path('users/signup', views.signup_view, name="signup"),
    path('auth/login/', views.login_view, name="login"),
    path('users/update/<int:user_id>/', views.update_view, name="update"),
    path('transactions/deposit/<int:user_id>', views.deposit, name="user_id"),
    path('transactions/transfer/<int:user_id>', views.transfers, name="transfers"),
    path('transactions/withdrawal/<int:user_id>', views.withdrawal, name="withdrawals"), 
    path('token/', TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path('token/refresh/', TokenRefreshView.as_view(), name="token_refresh"),
    

    
    
]