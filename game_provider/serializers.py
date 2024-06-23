from rest_framework.serializers import ModelSerializer
from .models import AdminAccountDetails, Transaction, Bet

class AdminAccountDetailsSerializer(ModelSerializer):
    
    class Meta:
        model = AdminAccountDetails
        fields = ["account_name", "bank_name", "account_number", "last_updated_at"]
        

class TransactionSerializer:
    
    class Meta:
        model = Transaction
        fields = ["id", "amount", "trans_type", "status", "created_at"]

class BetSerializer:
    
    class Meta:
        model = Bet
        fields = ["id", "game", "amount", "status", "created_at"]
        