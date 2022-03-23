from __future__ import unicode_literals
import email
# from sre_constants import BRANCH

from django.db import models
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.utils.translation import gettext_lazy as _
import jwt

# from datetime import datetime, timedelta

# from django.conf import settings
# from django.contrib.auth import get_user_model
from django.forms import model_to_dict

# User = get_user_model()

from .managers import UserManager
from django.utils import timezone


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
    phone = models.CharField(_('phone number'), unique=True, max_length=15)
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=30, blank=True)
    account_num = models.FloatField(_('account num'),  blank=True )
    bank_name = models.CharField(_('bank name'), max_length= 200, choices=BANK, blank=True)
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

    
    
class Token(models.Model):
    code = models.CharField(max_length=5000)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # expiry_date = models.DateTimeField()
    
    def __str__(self) -> str:
        return self._generate_jwt_token()
        # return f"{self.code} >>> {self.user.email}"
    
    
    # def is_expired(self):
    #     return timezone.now() > self.expiry_date



# class Client(models.Model):
#     name = models.CharField(max_length=250)
#     email = models.CharField(max_length=250)

#     def json_object(self):
#         return {
#             "name":self.name,
#             "address":self.email
#         }

#     def __str_(self):
# #         return self.name

# class Account(models.Model):
#     # email = models.EmailField()
#     user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name="account")   
#     date_created = models.DateTimeField(_('date created'), auto_now_add=True)

     
#     def __str__(self) -> str:
#         return self.user

#     @property
#     def account_num(self):
#         return model_to_dict(self.user)
    # def __str__(self) -> str:
    #     return f"{self.email}"
    
    
    # def is_expired(self):
    #     return timezone.now() > self.expiry_date


#     def json_object(self):
#         return {
#             "open_date":self.open_date,
#             "account_type":self.account_type,
#             "bank":self.bank

#         }

#     def __str__(self):
#         return self.account_type


# class Transfer(models.Model):
#     account = models.ForeignKey(Account,on_delete=models.CASCADE)
#     branch = models.ForeignKey(User,on_delete=models.CASCADE)

#     def json_object(self):
#         return {
#             "account":self.account,
#             "branch":self.branch
#         }

#     def __str__(self):
#         return "Account Transfered to {} Branch".format(self.branch.name)


# class Withdraw(models.Model):
#     amount = models.FloatField()
#     account = models.ForeignKey(Account,on_delete=models.CASCADE)


# class Deposit(models.Model):
#     amount = models.FloatField()
#     account = models.ForeignKey(Account,on_delete=models.CASCADE)
