from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from uuid import uuid4

# Model Schema

class UserDetails(models.Model):
    id = models.UUIDField(default=uuid4, primary_key=True, editable=False)
    phone_number = models.CharField(default="+1-0000000000", max_length=20)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="user_details")
    balance = models.FloatField(default=0)
    bonus = models.FloatField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.email}'s Details"
    
# Model signals
def create_user_detail(sender, instance, created, **kwargs):
    if created:
        UserDetails.objects.create(user=instance)
        print("created user detail")

post_save.connect(create_user_detail, sender=User)