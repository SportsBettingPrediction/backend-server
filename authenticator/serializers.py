from rest_framework.serializers import ModelSerializer, CharField
from django.contrib.auth.models import User
from .models import UserDetails

class UserDetailsSerializer(ModelSerializer):
    email = CharField(source='user.email')
    class Meta:
        model = UserDetails
        fields = ["id", "email", "balance", "bonus"]
        

class UserSerializer(ModelSerializer):
    
    class Meta:
        model = User
        fields = ["email"]
        