from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from uritemplate import partial
from .models import Deposit, Transfer, Withdraw
from .serializers import DepositSerializer, TransferSerializer, WithdrawSerializer
from account.serializers import UserSerializer
from drf_yasg.utils import swagger_auto_schema
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError, PermissionDenied


# Create your views here.

@swagger_auto_schema(methods=['PUT'] ,
                    request_body=DepositSerializer())
@api_view(['GET', 'PUT'])
def deposits(request, user_id):

    
    
   
    try:
        user = Deposit.objects.get(id=user_id)
    except Deposit.DoesNotExist:
        

        data = {
                'message' : 'failed',
                'error'  : f"Song with ID {user_id} does not exist."
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
        serializer = DepositSerializer(user, data=request.data, partial=True)
        if serializer.is_valid(): 
            amount = amount
            account_balance = account_balance + amount
                
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


@swagger_auto_schema(methods=['POST'] ,
                    request_body=TransferSerializer())
@api_view(['POST'])
def transfers(request):
    amount = amount
    account_balance = account_balance - amount

    if request.method == 'POST':
        serializer = TransferSerializer(data=request.data)
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

@swagger_auto_schema(methods=['POST'] ,
                    request_body=WithdrawSerializer())
@api_view(['POST'])
def withdrawals(request):
    amount = amount
    account_balance = account_balance - amount
    
    if request.method == 'POST':
        serializer = WithdrawSerializer(data=request.data)
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