from rest_framework.response import Response
from rest_framework.decorators import api_view

# Create your views here.
@api_view(["GET"])
def index(request):
    return Response(status=200, data={"message": "hello world"})