from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework.exceptions import ValidationError
from django.conf import settings
from account.models import User, Transfer, Withdraw



User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length = 255, write_only=True)
   
    account_balance = serializers.FloatField()
    class Meta:
        model = User
        fields = ['id','first_name', 'last_name','account_num', 'account_balance', 'email', 'password', 'phone','branch','bank_name','date_created']



class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(max_length=255)
    

class DepositSerializer(serializers.ModelSerializer):
    deposit_amount = serializers.FloatField()
    class Meta:
        model = User
        fields = ['id', 'deposit_amount', 'date_created']

   

class TransferSerializer(serializers.ModelSerializer):
    recipient_name = serializers.CharField(max_length=100)
    recipient_acc_num = serializers.FloatField()
    trans_amount = serializers.FloatField()
    class Meta:
        model = Transfer
        fields = ['trans_amount','recipient_acc_num','recipient_name']


class WithdrawSerializer(serializers.ModelSerializer):
    withdrawal_amount = serializers.FloatField()
    class Meta:
        model = Withdraw
        fields =  ['withdrawal_amount']
    
