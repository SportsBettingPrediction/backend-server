from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token

from django.contrib.auth.models import User

from .models import UserDetails
from .serializers import UserDetailsSerializer, UserSerializer

class LoginApiView(APIView):
    
    def post(self, request):
        email = request.data.get("email", None)
        phone_number = request.data.get("phone_number", None)
        password = request.data.get("password", None)
        is_email = bool(int(request.data.get("is_email", "1")))
        
        if (email == None or email == "") and is_email :
            return Response(status=400, data={"error_message": "required field not provided"})
        
        if (phone_number == "" or phone_number == None) and not is_email:
            return Response(status=400, data={"error_message": "required field not provided"})
        
        if password == "" or password == None:
            return Response(status=400, data={"error_message": "required field not provided"})
        
        
        try:
            user = User.objects.get(email=email) if is_email else UserDetails.objects.get(phone_number=phone_number).user
            
            if not user.check_password(password):
                return Response(status=401, data={"error_message": "invalid login details check and try again"})
            
            token = Token.objects.get(user=user)
            user_serializer = UserSerializer(user)
            user_details_serializer = UserDetailsSerializer(user.user_details)
       
        except UserDetails.DoesNotExist:
            return Response(status=401, data={"error_message": "user with provided phone number does not exist"})
        
        except User.DoesNotExist:
            return Response(status=401, data={"error_message": "user with provided email does not exist"})
        
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
                return Response(status=400, data={"error_message": "required field not provided"})
            
        if password != password_confirm:
            return Response(status=400, data={"error_message": "passwords do not match"})
        
        try:
            user = User.objects.create(first_name=first_name, last_name=last_name, username=email, email=email)
            user.set_password(password)
            user.save()
            
            user.user_details.phone_number = phone_number
            user.user_details.save()
            token = Token.objects.create(user=user)
            user_serializer = UserSerializer(user)
            user_details_serializer = UserDetailsSerializer(user.user_details)
            
            
        except Exception as e:
            return Response(status=500, data={"error_message": str(e)})
         
        return Response(status=200, data={"key": token.key, "user_details": {**user_serializer.data, **user_details_serializer.data}})