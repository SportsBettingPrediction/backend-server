from rest_framework.serializers import ModelSerializer
from django.contrib.auth.models import User
from .models import UserDetails

class UserDetailsSerializer(ModelSerializer):
    
    class Meta:
        model = UserDetails
        fields = ["id", "user", "balance", "bonus"]
        

class UserSerializer(ModelSerializer):
    
    class Meta:
        model = User
        fields = ["email", ]
        