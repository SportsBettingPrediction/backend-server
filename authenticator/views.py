from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token

from django.contrib.auth.models import User
from .serializers import UserDetailsSerializer, UserSerializer

class LoginApiView(APIView):
    
    def post(self, request):
        email = request.data.get("email", None)
        password = request.data.get("password", None)
        
        if email == None or email == "" or password == "" or password == None:
            return Response(status=400, data={"error_message": "required field not provided"})
        
        try:
            user = User.objects.get(email=email)
            
            if not user.check_password(password):
                return Response(status=401, data={"error_message": "invalid login details check and try again"})
            
            token = Token.objects.get(user=user)
            user_serializer = UserSerializer(user)
            user_details_serializer = UserDetailsSerializer(user.user_details)
        
        except User.DoesNotExist:
            return Response(status=401, data={"error_message": "user does not exist"})
        
        except Exception as e:
            return Response(status=500, data={"error_message": str(e)})
        
        return Response(status=200, data={"key": token.key, "user_details": {**user_serializer.data, **user_details_serializer.data}})
    
class SignUpApiView(APIView):
    
    def post(self, request):
        first_name = request.data.get('first_name', None)
        last_name = request.data.get('last_name', None)
        email = request.data.get('email', None)
        phone_number = request.data.get('phone_number', None)
        password = request.data.get('password', None)
        password_confirm = request.data.get('password_confirm', None)
        
        if (first_name == None or first_name == "") or \
            (last_name == None or last_name == "") or \
            (email == None or email == "") or \
            (phone_number == None or phone_number == "") or \
            (password == None or password == "") or \
            (password_confirm == None or password_confirm == ""):
                
        return Response(status=200, data={"message": "working"})