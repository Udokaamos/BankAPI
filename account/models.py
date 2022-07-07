from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.utils.translation import gettext_lazy as _


from .managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    BANK = (
        ("FirstBank", "FirstBank"),
        ("AccessBank", "AccessBank"),
        ("ZenithBank", "ZenithBank"),
        ("SterlingBank", "SterkingBank"),
        ("StanbicIBTCBank", "StanbicIBTC"),
        ("GTBank", "GTBank")

    )
    email = models.EmailField(_('email address'), unique=True)
    phone = models.FloatField(_('phone number'), unique=True, max_length=11)
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=30, blank=True)
    account_num = models.FloatField(_('account num'), blank=True, unique=True, default=0)
    account_type = models.CharField(max_length=355, blank=True)
    bank_name = models.CharField(_('bank name'), max_length= 200, choices=BANK, blank=True)
    account_balance = models.FloatField(_('account balance'), max_length= 50, null=True, blank=True)
    branch = models.CharField(_('branch name'), max_length=100, blank=True)
    branch_address = models.CharField(('branch address'), max_length=250)
    date_created = models.DateTimeField(_('date created'), auto_now_add=True)
    is_staff = models.BooleanField(_('staff'), default=False)
    is_admin = models.BooleanField(_('admin'), default=False)
    is_superuser = models.BooleanField(_('superuser'), default=False)
    is_active = models.BooleanField(_('active'), default=False)
   

    

    
    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['phone']

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')
        
    

    def __str__(self) -> str:
        return self.email


class Transfer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    recipient_name = models.CharField(max_length=50, blank=True)
    recipient_acc_num = models.FloatField()
    recipient_bank_name = models.CharField(max_length=50, blank=True)
    trans_amount = models.FloatField()
    

    

class Withdraw(models.Model):
    withdrawal_amount = models.FloatField()
   