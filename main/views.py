# from lib2to3.pgen2 import token
import random
from rest_framework.response import Response
from rest_framework import status 
from django.http import JsonResponse
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from .serializers import  UserSerializer, LoginSerializer, GenerateAccountSerializer
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

@api_view(['POST'])
@authentication_classes([BasicAuthentication])
def signup_view(request):
    
    if request.method == "POST":
    #Allows user to signup or create account
        serializer = UserSerializer(data=request.data) #deserialize the data
        
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
# @api_view(['GET'])
# @authentication_classes([BasicAuthentication])
# # @permission_classes([IsAdminUser])
# # def user_view(request):
    
#     elif request.method == 'GET':
#         # Get all the users in the database
#         all_users = User.objects.all()
        
#         serializer = UserSerializer(all_users, many=True)
        
#         data = {
#            "message":"successful",
#            "data": serializer.data
#         }
    
    
#         # return JsonResponse(data)
#         return Response(data, status=status.HTTP_200_OK)
   
        

@swagger_auto_schema(method='post', 
                    request_body=LoginSerializer())
@api_view(['POST'])
def login_view(request):

    if request.method == "POST":

        serializer = LoginSerializer(data=request.data)
        
        if serializer.is_valid():
            
            user = authenticate(email=serializer.validated_data['email'], password=serializer.validated_data['password'])
            
            if user: 
            
                data = {
                        'message' : 'success',
                        'data'  : model_to_dict(user, ['id', 
                                                    'first_name',
                                                    'last_name',
                                                    'email',
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

@swagger_auto_schema(methods=['POST'] ,
                    request_body=GenerateAccountSerializer())
@api_view(["POST"])
@authentication_classes([BasicAuthentication])
 # @permission_classes([IsAuthenticated])
def generate_acc_num(request):
    serializer = GenerateAccountSerializer(data=request.data)

    if serializer.is_valid():
        user = serializer.generate()
        user_serializer = UserSerializer(user)
        data = {
            'message' : 'account generated',
            'data' : user_serializer.data
        }
        return Response(data, status=status.HTTP_200_OK)
        
    else:
        data = {
            'message' : 'failed',
            'error'  : serializer.errors
        }
        return Response(data, status=status.HTTP_400_BAD_REQUEST)

    # user = request.user

    # if request.method == "POST":
    #     serializer = UserSerializer(user)
        
    #     data = {
    #        "message":"successful",
    #        "data": serializer.data
    #     }
    #     return Response(data, status=status.HTTP_200_OK)

    # elif request.method == "POST":        
    #     serializer = AccountSerializer(data=request.data)
            
  
    # for i in range(10):

    #     num = [str(i)]
    #     num = [str(i) for i in range(10)]
    #     acc = ['9']
    #     acc.extend([random.choice(num) for i in range(9)])
    #     acc_num = "".join(acc)
        
    #     if acc_num in user.keys():
    #         return generate_acc_num()
        
    #     # return acc_num
    #     data = {
    #     "message":"successful",
    #     "data": serializer.data
    #     }

    #     return Response(data, status=status.HTTP_200_OK)

    # else:
    #             data = {
    #                     'message' : 'Please enter a valid email and password'
    #                 }
    #             return Response(data, status=status.HTTP_401_UNAUTHORIZED)

# @api_view
# def withdraw_view(request): 
#     user = request.user   
#     if request.method == 'PUT':
#         serializer = DepositSerializer(user, data=request.data, partial=True)
#         if serializer.is_valid(): 
#             if 'password' in serializer.validated_data.keys():
#                 raise ValidationError(detail={
#                     "message":"Edit password action not allowed"
#                 }, code=status.HTTP_403_FORBIDDEN)
                
#             serializer.save()
#             data = {
#                 'message' : 'success',
#                 'data'  : serializer.data
#             }
#             return Response(data, status=status.HTTP_202_ACCEPTED)
#         else:
#             data = {
#                 'message' : 'failed',
#                 'error'  : serializer.errors
#             }
#             return Response(data, status=status.HTTP_400_BAD_REQUEST)
        
#     elif request.method=="DELETE":
#         user.delete()
        
#         return Response({}, status=status.HTTP_204_NO_CONTENT)


# @swagger_auto_schema(method='post', 
#                 request_body=TokenObtainPairSerializer())
# @api_view(['POST'])
# def as_view(request):
#     serializer = TokenObtainPairSerializer(data=request.data)

#     if serializer.is_valid(): #validate the data that was passed
#         token = serializer.view()
#         token_serializer = TokenObtainPairSerializer()
#         data = {
#             'message' : 'success',
#             'data'  : serializer.data
#         }
#         return Response(data, status=status.HTTP_201_CREATED)
#     else:
#         data = {
#             'message' : 'failed',
#             'error'  : serializer.errors
#         }
#         return Response(data, status=status.HTTP_400_BAD_REQUEST)




# @swagger_auto_schema(methods=['put'] ,
#                     request_body=DepositSerializer())
# @api_view(['GET', 'PUT', 'DELETE'])
# @authentication_classes([BasicAuthentication])
# @permission_classes([IsAuthenticated])
# def deposit(request, account_details):

    
#     # try:
#     #     song = Song.objects.get(id=song_id)
#     # except Song.DoesNotExist:

#     #     data = {
#     #         'message' : 'failed',
#     #         'error'  : f"Song with ID {song_id} does not exist."
#     #     }
#     #     return Response(data, status=status.HTTP_404_NOT_FOUND)
    
#     if request.method == "PUT":
#         deposits = Deposit.objects.get(id=account_details)
#         serializer = DepositSerializer(deposits)
        
#         data = {
#            "message":"successful",
#            "data": serializer.data
#         }
    
    
#         return Response(data, status=status.HTTP_200_OK)
    
#     elif request.method == 'PUT':
#         serializer = SongSerializer(song, data=request.data, partial=True)
#         if serializer.is_valid():
                
#             serializer.save()
#             data = {
#                 'message' : 'success',
#                 'data'  : serializer.data
#             }
#             return Response(data, status=status.HTTP_202_ACCEPTED)
#         else:
#             data = {
#                 'message' : 'failed',
#                 'error'  : serializer.errors
#             }
#             return Response(data, status=status.HTTP_400_BAD_REQUEST)
        
#     elif request.method=="DELETE":
#         song.delete()
        
#         return Response({}, status=status.HTTP_204_NO_CONTENT)