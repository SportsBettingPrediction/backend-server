from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from django.contrib.auth.models import User

from .models import UserDetails, ProfileImage
from .serializers import UserDetailsSerializer, UserSerializer
from game_provider.serializers import AdminAccountDetails, AdminAccountDetailsSerializer

class LoginApiView(APIView):
    
    def post(self, request):
        email = request.data.get("email", None)
        phone_number = request.data.get("phone_number", None)
        password = request.data.get("password", None)
        is_email = request.data.get("is_email", True)
        
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
            admin_account_details_serializer = AdminAccountDetailsSerializer(AdminAccountDetails.objects.all().last())
       
        except UserDetails.DoesNotExist:
            return Response(status=401, data={"error_message": "user with the provided phone number does not exist"})
        
        except User.DoesNotExist:
            return Response(status=401, data={"error_message": "user with the provided email does not exist"})
        
        except Exception as e:
            return Response(status=500, data={"error_message": str(e)})
        
        return Response(status=200, data={
                                            "key": token.key, 
                                            "user_details": {**user_serializer.data, **user_details_serializer.data}, 
                                            "admin_account_details": admin_account_details_serializer.data
                                            })
    
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
            
            token = Token.objects.get(user=user)
            user_serializer = UserSerializer(user)
            user_details_serializer = UserDetailsSerializer(user.user_details)
            admin_account_details_serializer = AdminAccountDetailsSerializer(AdminAccountDetails.objects.all().last())
            
        except Exception as e:
            return Response(status=500, data={"error_message": str(e)})
         
        return Response(status=200, data={
                                            "key": token.key, 
                                            "user_details": {**user_serializer.data, **user_details_serializer.data}, 
                                            "admin_account_details": admin_account_details_serializer.data
                                            })
        
class UpdateProfileImageView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        new_img_id = request.data.get("img_id", None)
        
        if new_img_id == None or new_img_id == "":
            return Response(status=400, data={"error_message": "required field not provided"})
        
        try:
            user_details = request.user.user_details
            if str(user_details.profile_img.id) == str(new_img_id):
                return Response(status=400, data={"error_message": "new profile image is the same as current profile image"})
            
            profile_img = ProfileImage.objects.get(id=new_img_id)
            user_details.profile_img = profile_img
            user_details.save()
            
            user_serializer = UserSerializer(request.user)
            user_details_serializer = UserDetailsSerializer(user_details)
            
        except ProfileImage.DoesNotExist:
            return Response(status=400, data={"error_message": "profile image with the provided ID does not exist"})
        
        except Exception as e:
            return Response(status=500, data={"error_message": str(e)})
        
        return Response(status=200, data={"user_details": 
                                                    {
                                                        "user_details": {**user_serializer.data, **user_details_serializer.data}, 
                                                    }
                                                })

class UpdatePhoneNumberApiView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        phone_number = request.data.get("phone_number", None)
        
        if phone_number == None or phone_number == "":
            return Response(status=400, data={"error_message": "required field not provided"})
        
        try:
            user_details = request.user.user_details
            if str(user_details.phone_number) == str(phone_number):
                return Response(status=400, data={"error_message": "new phone number is the same as current phone number"})
            
            user_details.phone_number = phone_number
            user_details.save()
            
            user_serializer = UserSerializer(request.user)
            user_details_serializer = UserDetailsSerializer(user_details)
            
        except Exception as e:
            return Response(status=500, data={"error_message": str(e)})
        
        return Response(status=200, data={"user_details": {**user_serializer.data, **user_details_serializer.data}})

class UpdatePasswordApiView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        password_old = request.data.get("password_old", None)
        password_new = request.data.get("password_new", None)
        password_confirm = request.data.get("password_confirm", None)
        
        if (password_old == None or password_old == "") \
            (password_new == None or password_new == "") \
            (password_confirm == None or password_confirm == ""):
            return Response(status=400, data={"error_message": "required field not provided"})
        
        try:
            user_details = request.user.user_details
            
            if not request.user.check_password(password_old):
                return Response(status=401, data={"error_message": "incorrect password"})
            
            if str(password_old) == str(password_new):
                return Response(status=400, data={"error_message": "new password is the same as current password"})
            
            if str(password_confirm) != str(password_new):
                return Response(status=400, data={"error_message": "password could not be confirmed. check details and try again"})
            
            request.user.set_password(password_new)
            request.user.save()
            
            user_serializer = UserSerializer(request.user)
            user_details_serializer = UserDetailsSerializer(user_details)
            
        except Exception as e:
            return Response(status=500, data={"error_message": str(e)})
        
        return Response(status=200, data={"user_details": {**user_serializer.data, **user_details_serializer.data}})