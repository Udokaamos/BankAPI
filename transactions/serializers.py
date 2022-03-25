from rest_framework import serializers

from transactions.models import Deposit, Transfer, Withdraw


class DepositSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Deposit
        fields = '__all__'
        
        

class TransferSerializer(serializers.ModelSerializer):
    # song_detail = serializers.ReadOnlyField()
    
    class Meta:
        model = Transfer
        fields = '__all__'
        # depth=1

class WithdrawSerializer(serializers.ModelSerializer):
    # song_detail = serializers.ReadOnlyField()
    
    class Meta:
        model = Withdraw
        fields = '__all__'
        # depth=1