from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from .serializers import Transaction, TransactionSerializer

# Create your views here.
class TransactionApiView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        transaction_query_set = Transaction.objects.filter(user=request.user).order_by("-created_at")
        transaction_set_serializer = TransactionSerializer(transaction_query_set, many=True)
        return Response(status=200, data={"transactions": transaction_set_serializer.data})
    
    
