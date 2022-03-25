# from lib2to3.pgen2 import token
import random
# from typing_extensions import Self
from rest_framework.response import Response
from rest_framework import status 
from django.http import JsonResponse
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from .serializers import  UserSerializer, LoginSerializer
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
@authentication_classes([BasicAuthentication])
# @permission_classes([IsAdminUser])
def user_view(request):

    # try:
    #     user = User.objects.get(id=user_id)
    # except User.DoesNotExist:

    #     data = {
    #         'message' : 'failed',
    #         'error'  : f"Post with ID {user_id} does not exist."
    #     }
    #     return Response(data, status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        # Get all the users in the database
        all_users = User.objects.all()
        
        serializer = UserSerializer(all_users, many=True)
        
        data = {
           "message":"successful",
           "data": serializer.data
        }
    
    
        # return JsonResponse(data)
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

# account_number = generate_acc_num()

# print(account_number)

@api_view(['POST'])
@authentication_classes([BasicAuthentication])
def signup_view(request):

    def generate_acc_num():
        num = [str(i) for i in range(10)]
        acc = ['9']
        acc.extend([random.choice(num) for i in range(9)])
        account_num = "".join(acc)
        
        # if account_num in user_data.keys():
        #     return generate_acc_num()
        
        return account_num
    user=request.data
    user_data = {
        'first_name': user['first_name'],
        'last_name': user['last_name'], 
        'account_num': generate_acc_num(), 
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
# @permission_classes([IsAuthenticated])
def update_view(request, user_id):

    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:

        data = {
            'message' : 'failed',
            'error'  : f"User with ID {user_id} does not exist."
        }
        return Response(data, status=status.HTTP_404_NOT_FOUND)
    
    if request.method == "GET":
        serializer = UserSerializer(user)
        
        data = {
           "message":"successful",
           "data": serializer.data
        }
    
    
        return Response(data, status=status.HTTP_200_OK)

    if request.method == 'PUT':
        # user=request.data
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            # if 'password' in serializer.validated_data.keys():
            #     raise ValidationError(detail={
            #         "message":"Edit password action not allowed"
            #     }, code=status.HTTP_403_FORBIDDEN)
                    
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
# @authentication_classes([BasicAuthentication])
# @permission_classes([IsAuthenticated])
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
                                                    'phone',
                                                    'is_admin'])
                    }
                return Response(data, status=status.HTTP_201_CREATED)
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
    
    


# @swagger_auto_schema(methods=['POST'] ,
#                     request_body=AccountSerializer())
# @api_view(['POST'])
# @authentication_classes([BasicAuthentication])
# # @permission_classes([IsAuthenticated])
# def generate_acc_num(request):
#     user= request.user
#     if request.method == "POST":
#         serializer = AccountSerializer(user)
        
#         data = {
#            "message":"successful",
#            "data": serializer.data
#        }

# @swagger_auto_schema(methods=['POST'] ,
#                     request_body=LoginSerializer())
# @api_view(["POST"])
# @authentication_classes([BasicAuthentication])
#  # @permission_classes([IsAuthenticated])
# def generate_acc_num(request, account_num):
    
#     if request.method == "POST":

#         serializer = LoginSerializer(data=request.account_num)
        
#         if serializer.is_valid():
            
#             user = authenticate(email=serializer.validated_data['email'], password=serializer.validated_data['password'])
            
#             if user: 
#                 user = User.objects.create(account_num)
#                 num = [str(i) for i in range(10)]
#                 account = ['9']
#                 account.extend([random.choice(num) for i in range(9)])
#                 account_num = "".join(account)
#                 data = {
#                         'message' : 'success',
#                         'data'  : model_to_dict(user, ['id', 
#                                                     'first_name',
#                                                     'last_name',
#                                                     'email',
#                                                     'phone',
#                                                     'account_num',
#                                                     'is_admin'])
#                     }
#                 return Response(account_num, status=status.HTTP_201_CREATED)
#             else:
#                 data = {
#                         'message' : 'Please enter a valid email and password'
#                     }
#                 return Response(data, status=status.HTTP_401_UNAUTHORIZED)
#         else:
#             data = {
#                 'message' : 'failed',
#                 'error'  : serializer.errors
#             }
#             return Response(data, status=status.HTTP_400_BAD_REQUEST)




# @swagger_auto_schema(methods=['POST'] ,
#                     request_body=MenuSerializer())
# @api_view(['POST'])
# @authentication_classes([BasicAuthentication])
# @permission_classes([IsAuthenticated])
# def make_carts(request,vendor_user_id): 
#     # add food to cart
#     user=request.user  #user creating cart 
#     if user.is_customer==False:
#         raise PermissionDenied(detail={"message":f"Permission Denied. Only customers can perform this action"})
#     if request.method == 'POST':
#         serializer = CartSerializer(data=request.data)
#         if serializer.is_valid(): 
#             if "user" in serializer.validated_data.keys():
#                 serializer.validated_data.pop("user")  
#             food = serializer.validated_data["food"]
#             ven=User.objects.filter(id=vendor_user_id)
#             if ven.exists():
#                 pass
#             else:
#                 data = {
#                 'message' : 'Vendor does not exist',
#             }
#                 return Response(data, status=status.HTTP_400_BAD_REQUEST)

#             check = Menu.objects.filter(food=food,user=User.objects.get(id=vendor_user_id))
#             if check.exists():
#                 pass
#             else:
#                 raise PermissionDenied(detail={"message":f"Vendor {vendor_user_id} does not have this item."}) 

            
#             if len(Cart.objects.filter(user=user)) != 0:
#                 diff_vens=Cart.objects.filter(user=user).first() #checks if the item has a diff vendor from what is already in cart
#                 if diff_vens.food.user.id != vendor_user_id:
#                     data = {
#                     'message' : 'Cart can only contain food from one vendor',
#                 }
#                     return Response(data, status=status.HTTP_400_BAD_REQUEST)


            

#             cart = Cart.objects.create(user=user, food=food)
#             new_serializer = CartSerializer(cart)
            
#             data = {
#                 'message' : 'success',
#                 'data'  : new_serializer.data
#             }
#             return Response(data, status=status.HTTP_202_ACCEPTED)
#         else:
#             data = {
#                 'message' : 'failed',
#                 'error'  : serializer.errors
#             }
#             return Response(data, status=status.HTTP_400_BAD_REQUEST)