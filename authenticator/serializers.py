from rest_framework.serializers import ModelSerializer, CharField
from django.contrib.auth.models import User
from .models import UserDetails, ProfileImage


class ProfileImageSerializer(ModelSerializer):

    class Meta:
        model = ProfileImage
        fields = ["id", "url"]

class UserDetailsSerializer(ModelSerializer):
    email = CharField(source='user.email')
    profile_pic = CharField(source='profile_img.url')
    class Meta:
        model = UserDetails
        fields = ["id", "email", "balance", "bonus", "profile_pic", "created_at"]
        

class UserSerializer(ModelSerializer):
    
    class Meta:
        model = User
        fields = ["email"]
        