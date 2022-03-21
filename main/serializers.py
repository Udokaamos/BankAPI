# import code
# import email
import random
# from lib2to3.pgen2 import token
# from pyexpat import model
# from pyexpat import model
# from tokenize import Token
# import email
from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework.exceptions import ValidationError
# from BankAPI.main.models import Account
from main.models import User, Account
# from django.core.mail import send_mail
# import jwt
# from datetime import datetime, timedelta
# from django.conf import settings


User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length = 255, write_only=True)
    # email = serializers.EmailField()
    # acc_num = serializers.FloatField(read_only=True)
    class Meta:
        model = User
        #fields = '__all__'
        fields = ['id','first_name', 'last_name', 'email', 'password', 'phone','branch','bank_name','date_created']



class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(max_length=255)
    # class Meta:
    #     model = User
#         fields = '__all__'

class GenerateAccountSerializer(serializers.ModelSerializer):
    acc_num = serializers.FloatField()
    # email = serializers.EmailField()
    # password = serializers.CharField(max_length=255)
    class Meta:
        model = Account
        fields = ['acc_num']

    # @property
    def generate(self):
        acc_num = self.validated_data('acc_num')
        try:
            acc_num = Account.objects.get(acc_num)
            num = [str(i) for i in range(10)]
            acc = ['9']
            acc.extend([random.choice(num) for i in range(9)])
            acc_num = "".join(acc)
        except User.DoesNotExist:
            raise ValidationError(detail={
                "error":"Invalid User"
            }) 

        except Exception:
            Account.objects.filter(acc_num).delete()
            raise ValidationError(detail={
                "error":"unable to generate account number"
            })
        # if account_num in user.keys():
            
        #     return generate_acc_num()




# class ClientSerializer(serializers.Serializer):
#     email = serializers.EmailField()
#     password = serializers.CharField(max_length = 255)
    # class Meta:
    #     model = Client

    #     fields = '__all__'
        #   fields = ['id','first_name', 'last_name', 'email', 'password', 'phone','branch','bank','date_created']



# class TokenObtainPairSerializer(serializers.Serializer):
#     code= serializers.CharField(max_length=200, read_only=True)
#     class Meta:
#         model = Token
    

    
    # @property
    # def token(self):
    #     """
    #     Allows us to get a user's token by calling `user.token` instead of
    #     `user.generate_jwt_token().

    #     The `@property` decorator above makes this possible. `token` is called
    #     a "dynamic property".
    #     """
    #     return self._generate_jwt_token()

    # def get_full_name(self):
    #     """
    #     This method is required by Django for things like handling emails.
    #     Typically this would be the user's first and last name. Since we do
    #     not store the user's real name, we return their username instead.
    #     """
    #     return self.username

    # def get_short_name(self):
    #     """
    #     This method is required by Django for things like handling emails.
    #     Typically, this would be the user's first name. Since we do not store
    #     the user's real name, we return their username instead.
    #     """
    #     return self.username

    # def _generate_jwt_token(self):
    #     """
    #     Generates a JSON Web Token that stores this user's ID and has an expiry
    #     date set to 60 days into the future.
    #     """
    #     dt = datetime.now() + timedelta(days=60)

    #     token = jwt.encode({
    #         'id': self.pk,
    #         'exp': int(dt.strftime('%s'))
    #     }, settings.SECRET_KEY, algorithm='HS256')

    #     return token.decode('utf-8')

# class AccountSerializer(serializers.ModelSerializer):
#     # email = serializers.EmailField()
#     # password = serializers.CharField(max_length=255)
#     account_num = serializers.FloatField( read_only=True)
#     class Meta:
#         model = Account

#         fields = '__all__'
#         # fields = ['email','account_num']


    

# class DepositSerializer(serializers.Serializer):
#     name = serializers.CharField(max_length=200)
#     amount = serializers.FloatField()
#     account = serializers.FloatField()

#     class Meta:
#         model = Deposit
    
#     def json_object(self):
#         return {
#             "amount":self.amount,
#             "account":self.account
#         }

#     def __str__(self):
#         return "Amount Deposited to {} Account".format(self.account.name)


# class TransferSerialzer(serializers.Serializer):
#      account = serializers.FloatField()
#      amount = serializers.FloatField()

#      class Meta:
#          model = Transfer

# class WithdrawSerializer(serializers.Serializer):
#     amount = serializers.FloatField()
#     account = serializers.FloatField()

#     class Meta:
#         model = Withdraw
    

# class VerifyTokenSerializer(serializers.Serializer):
#     token=serializers.CharField(max_length=255, read_only=True)
    
    
#     def verify(self):
#         token = self.validated_data['token']
#         try:
#             token = token.objects.get(code=token)
#         except token.DoesNotExist:
#             raise ValidationError(detail={
#                 "error":"Invalid TOKEN"
#             })
#         except Exception:
#             token.objects.filter(code=token).delete()
#             raise ValidationError(detail={
#                 "error":"Unable to fetch TOKEN"
#             })
            
        
#         if token.is_expired():
#             raise ValidationError(detail={
#                 "error":"TOKEN Expired"
#             })
#         else:
#             if token.user.is_active != True:
#                 token.user.is_active=True
#                 token.user.save()
#                 return token.user
#             else:
#                 raise ValidationError(detail={
#                 "error":"User with this token already active"
#             })
                
                
                
# class ResendTokenSerializer(serializers.Serializer):
#     email = serializers.EmailField()
    
    
#     def get_token(self):
#         email = self.validated_data['email']
        
#         if User.objects.filter(email=email, is_active=False).exists():
#             user = User.objects.get(email=email)
#             token, expiry_date = get_token(255)
            
#             token.objects.create(code=token, user=user, expiry_date=expiry_date)
#             message= f"""Welcome {user.first_name}!
# Your activation TOKEN is {token}.
# Expires in 2 minutes. 
# Regards,
# AdubaFX"""

#             send_mail(
#                 subject="NEW OTP VERIFICATION CODE",
#                 message=message,
#                 from_email='Aduba from AbokiFX',
#                 recipient_list=[user.email]
#             )
            
#             return {"message":"please check your email for new otp"}
#         else:
#             raise ValidationError(detail={
#                     "error":"Unable to get a user with this email"
#                 })