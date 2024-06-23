from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from datetime import datetime

from .serializers import Transaction, TransactionSerializer, Bet, BetSerializer

# Create your views here.
class TransactionApiView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        transaction_query_set = Transaction.objects.filter(user=request.user).order_by("-created_at")
        transaction_set_serializer = TransactionSerializer(transaction_query_set, many=True)
        return Response(status=200, data={"transactions": transaction_set_serializer.data})
    
    def post(self, request):
        trans_time = request.data.get("trans_time", None)
        trans_type = request.data.get("trans_type", None)
        trans_status = request.data.get("trans_status", None)
        
        transactions = Transaction.objects.filter(user=request.user).order_by("-created_at")
        if transactions.count() > 0:
            if trans_type != None:
                transactions = transactions.filter(trans_type=trans_type)
                
            if trans_status != None:
                transactions = transactions.filter(trans_status=trans_status)
            
            if trans_time != None:
                current_time = datetime.now().timestamp()
                filter_start_time = current_time - int(trans_time)
                transactions = list(filter(lambda trans: filter_start_time <= trans.created_at.timestamp()))
        
        transactions_serializer = TransactionSerializer(transactions, many=True)
        return Response(status=200, data={"transactions": transactions_serializer.data})
    
class BetHistoryApiView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        bet_query_set = Bet.objects.filter(user=request.user).order_by("-created_at")
        bet_set_serializer = BetSerializer(bet_query_set, many=True)
        return Response(status=200, data={"bet_history": bet_set_serializer.data})
    
    def post(self, request):
        bet_time = request.data.get("bet_time", None)
        bet_game = request.data.get("bet_game", None)
        
        bets = Bet.objects.filter(user=request.user).order_by("-created_at")
        if bets.count() > 0:
                
            if bet_game != None:
                bets = bets.filter(game=bet_game)
            
            if bet_time != None:
                current_time = datetime.now().timestamp()
                filter_start_time = current_time - int(bet_time)
                bets = list(filter(lambda bet: filter_start_time <= bet.created_at.timestamp()))
        
        bet_serializer = BetSerializer(bets, many=True)
        return Response(status=200, data={"bet_history": bet_serializer.data})
    
    
class WithdrawalApiView(APIView):
    
    def post(self, request):
        # amount = request.data.("amount", None)
        # account_number = request.data("account_number")
        return Response(status=200)

class DepositApiView(APIView):
    
    def post(self, request):
        return Response(status=200)
    
