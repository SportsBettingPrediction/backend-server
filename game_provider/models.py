from django.db import models
from django.contrib.auth.models import User

from uuid import uuid4

# Create your models here.
class AdminAccountDetails(models.Model):
    account_name = models.CharField(max_length=50)
    bank_name = models.CharField(max_length=50)
    account_number = models.CharField(max_length=20)
    telegram_link = models.CharField(max_length=200, default="")
    last_updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return "Admin Account Details"
    
    
class Transaction(models.Model):
    id = models.UUIDField(default=uuid4, primary_key=True, editable=False)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    amount = models.FloatField()
    trans_type = models.CharField(max_length=20, choices=[("withdrawal", "WITHDRAWAL"), ("deposit", "DEPOSIT")])
    status = models.CharField(max_length=20, choices=[("pending", "PENDING"), ("successful", "SUCCESSFUL"), ("failed", "FAILED")])
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"USER: {self.user.username}\tTYPE: {self.trans_type}\tAMOUNT: ₦{self.amount}"
    
# class 