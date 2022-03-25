from django.urls import path
from . import views


urlpatterns = [
    path('transactions/deposits/<int:user_id>/', views.deposits, name="deposits"),
    path('transactions/transfers', views.transfers, name="transfers"),
    path('transactions/withdrawals', views.withdrawals, name="withdrawals")
    
]