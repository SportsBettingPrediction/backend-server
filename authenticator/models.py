from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save

from rest_framework.authtoken.models import Token
from uuid import uuid4

# Model Schema

class ProfileImage(models.Model):
    id = models.UUIDField(default=uuid4, primary_key=True, editable=False)
    url = models.CharField(max_length=200, default="")

class UserDetails(models.Model):
    id = models.UUIDField(default=uuid4, primary_key=True, editable=False)
    phone_number = models.CharField(default="+1-0000000000", max_length=20)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="user_details")
    balance = models.FloatField(default=0)
    bonus = models.FloatField(default=0)
    profile_img = models.ForeignKey(ProfileImage, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.email}'s Details"
    
# Model Signals
def create_user_detail(sender, instance, created, **kwargs):
    if created:
        UserDetails.objects.create(user=instance)
        Token.objects.create(user=instance)

post_save.connect(create_user_detail, sender=User)