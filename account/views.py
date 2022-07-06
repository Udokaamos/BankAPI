import random
from tokenize import String
from typing_extensions import Self
from unicodedata import name
from rest_framework.response import Response
from rest_framework import status 
from django.http import JsonResponse
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from .serializers import  UserSerializer, LoginSerializer, WithdrawSerializer, TransferSerializer, DepositSerializer
from django.contrib.auth import get_user_model
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.contrib.auth import authenticate
from django.forms import model_to_dict
from rest_framework.exceptions import ValidationError
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser



User = get_user_model()



@api_view(['GET'])
def user_view(request):
    
    if request.method == 'GET':
        # Get all the users in the database
        all_users = User.objects.all()
        
        serializer = UserSerializer(all_users, many=True)
        
        data = {
           "message":"successful",
           "data": serializer.data
        }
    
        return Response(data, status=status.HTTP_200_OK)
    


@swagger_auto_schema(method='post', 
                    request_body=UserSerializer(),
                    operation_description="This is a function to create new users.",
                    responses= {201: openapi.Response("""An example success response is:
                    ``{
                        "message": "successful",
                        "data": [
                            {
                                "id": 1,
                                "first_name": "Test",
                                "last_name": "User",
                                "email": "test@user.com",
                                "phone": "234123456789",
                                "date_joined":"2022-01-26T10:33:45.239782Z"
                            }
                        ]
                    }``"""),
                        400: openapi.Response("""An example failure is:
                        ``{
                        "message": "failed",
                        "error": {
                            "email": [
                            "This field is required."
                            ],
                            "password": [
                            "This field is required."
                            ],
                            "phone": [
                            "This field is required."
                            ]
                        }``""")
                    }
)



@api_view(['POST'])
@authentication_classes([BasicAuthentication])
def signup_view(request):

    def generate_acc_num():
        num = [str(i) for i in range(10)]
        acc = ['9']
        acc.extend([random.choice(num) for i in range(9)])
        account_num = "".join(acc)
        
        
        return account_num
    user=request.data
    user_data = {
        'first_name': user['first_name'],
        'last_name': user['last_name'], 
        'account_num': generate_acc_num(), 
        'account_balance': user['account_balance'],
        'email': user['email'],
        'password':user['password'], 
        'phone': user['phone'], 
        'branch': user['branch'], 
        'bank_name': user['bank_name']
    }

    
    if request.method == "POST":
    #Allows user to signup or create account
        serializer = UserSerializer(data=user_data) #deserialize the data
        
        if serializer.is_valid(): #validate the data that was passed 
            serializer.save()
            data = {
                'message' : 'success',
                'data'  : serializer.data
            }
            return Response(data, status=status.HTTP_201_CREATED)
        else:
            data = {
                'message' : 'failed',
                'error'  : serializer.errors
            }
            return Response(data, status=status.HTTP_400_BAD_REQUEST)

@swagger_auto_schema(methods=['PUT'] ,
                    request_body=UserSerializer())
@api_view(['GET','PUT','DELETE'])
@authentication_classes([BasicAuthentication])
def update_view(request, user_id):

    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:

        data = {
            'message' : 'failed',
            'error'  : f"User with ID {user_id} does not exist."
        }
        return Response(data, status=status.HTTP_404_NOT_FOUND)
    user = request.user
    if request.method == "GET":
        serializer = UserSerializer(user)
        
        data = {
           "message":"successful",
           "data": serializer.data
        }
    
    
        return Response(data, status=status.HTTP_200_OK)

    elif request.method == 'PUT':
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
                    
            serializer.save()
            data = {
                'message' : 'success',
                'data'  : serializer.data
            }
            return Response(data, status=status.HTTP_202_ACCEPTED)
        else:
            data = {
                'message' : 'failed',
                'error'  : serializer.errors
            }
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
            
    elif request.method=="DELETE":
        user.delete()
        
        return Response({}, status=status.HTTP_204_NO_CONTENT)   

        

@swagger_auto_schema(method='post', 
                    request_body=LoginSerializer())
@api_view(['POST'])
def login_view(request):
    serializer = LoginSerializer(data=request.data)

    if request.method == "POST":

       
        
        if serializer.is_valid():
            
            user = authenticate(email=serializer.validated_data['email'], password=serializer.validated_data['password'])
            
            if user: 
            
                data = {
                        'message' : 'success',
                        'data'  : model_to_dict(user, ['id', 
                                                    'first_name',
                                                    'last_name',
                                                    'email',
                                                    'account_num',
                                                    'account_balance',
                                                    'phone',
                                                    'is_admin'])
                    }
                return Response(data, status=status.HTTP_200_OK)
            else:
                data = {
                        'message' : 'Please enter a valid email and password'
                    }
                return Response(data, status=status.HTTP_401_UNAUTHORIZED)
        else:
            data = {
                'message' : 'failed',
                'error'  : serializer.errors
            }
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
    
    

@swagger_auto_schema(methods=['POST'] ,
                    request_body=DepositSerializer())
@api_view([ 'POST'])
@authentication_classes([BasicAuthentication])
def deposit(request, user_id):


    if request.method == "POST":

        for user in User.objects.all():
            if user.id == user_id:
                user_data = {
                    'account_balance': request.data['deposit_amount'] + user.account_balance,
                    'id': user_id,
                    'email': user.email,
                    'phone': user.phone,
                    'password': user.password
                    
                }

                deposit_data = {
                    'deposit_amount': request.data['deposit_amount'],
                    'id': user_id
                }

                
                user_serializer = UserSerializer(instance=user, data=user_data)
                deposit_serializer = DepositSerializer(instance=user, data=deposit_data)
                if user_serializer.is_valid():
    
                #Allows user to signup or create account

                
                    if deposit_serializer.is_valid(): #validate the data that was passed
                        deposit_serializer.validated_data.update={
                            'account_balance'
                            }
                        
            
                        deposit_serializer.save(),
                        user_serializer.save()
                        data = {
                            'message' : 'success',
                            'data'  : deposit_serializer.data
                        }
                        
                        return Response(data, status=status.HTTP_201_CREATED)
                    else:
                        data = {
                            'message' : 'failed',
                            'error'  : deposit_serializer.errors
                        }
                        return Response(data, status=status.HTTP_400_BAD_REQUEST)



@swagger_auto_schema(methods=['POST'] ,
                    request_body=TransferSerializer())
@api_view(['POST'])
def transfers(request, user_id):

    if request.method == "POST":
        for user in User.objects.all():
            if user.id == user_id:
                user_data = {
                    'account_balance': user.account_balance - request.data['trans_amount'],
                    'id': user_id,
                    'email': user.email,
                    'phone': user.phone,
                    'password': user.password
                }

                transfer_data = {
                    'recipient_name': request.data['recipient_name'],
                    'recipient_acc_num': request.data['recipient_acc_num'],
                    'trans_amount': request.data['trans_amount'],
                    'id': user_id
                }
            
                user_serializer = UserSerializer(instance=user, data=user_data)
        
                transfer_serializer = TransferSerializer(instance=user, data=transfer_data)
                if user_serializer.is_valid():
                    
                    if transfer_serializer.is_valid():   
                        if  user.account_balance >= request.data['trans_amount']: 
                            transfer_serializer.save(),
                            user_serializer.save()
                            data = {
                                'message' : 'Transfer Successful',
                                'data'  : transfer_serializer.data
                                
                            }
                            return Response(data, status=status.HTTP_202_ACCEPTED)
        
                            
                        elif request.data['trans_amount'] > user.account_balance:
                            data = {
                                'message' : 'failed',
                                'error'  : 'Transfer amount must not be greater than the ledger balance.'
                            }
                            return Response(data, status=status.HTTP_403_FORBIDDEN)

                        
                    else:
                        data = {
                            'message' : 'failed',
                            'error'  : transfer_serializer.errors
                            
                        }
                        return Response(data, status=status.HTTP_400_BAD_REQUEST)

@swagger_auto_schema(methods=['POST'] ,
                    request_body=WithdrawSerializer())
@api_view(['POST'])
def withdrawal(request, user_id):
    
    
    if request.method == 'POST':
    
        for user in User.objects.all():
            if user.id == user_id:
                user_data = {
                    'account_balance': user.account_balance - request.data['withdrawal_amount'],
                    'id': user_id,
                    'email': user.email,
                    'phone': user.phone,
                    'password': user.password

                }

                withdrawal_data = {
                    'withdrawal_amount': request.data['withdrawal_amount'],
                    'id': user_id
                }

                
                user_serializer = UserSerializer(instance=user, data=user_data)
                withdrawal_serializer = WithdrawSerializer(instance=user, data=withdrawal_data)
                if user_serializer.is_valid():
                    
                    if withdrawal_serializer.is_valid(): 
                        # withdrawal_serializer.save()
                        if user.account_balance >= request.data['withdrawal_amount']:  
                            withdrawal_serializer.save(),
                            user_serializer.save()
                            data = {
                                'message' : 'successful withdrawal',
                                'data'  : withdrawal_serializer.data
                            }
                            return Response(data, status=status.HTTP_200_OK)
                        
                     

                        elif request.data['withdrawal_amount'] > user.account_balance:
                            data = {
                                'message' : 'failed',
                                'error'  :  f' Insufficient funds!!'
                            }
                            return Response(data, status=status.HTTP_403_FORBIDDEN)

                    else:
                        data = {
                            'message' : 'failed',
                            'error'  : withdrawal_serializer.errors
                        }
                        return Response(data, status=status.HTTP_400_BAD_REQUEST)

                
