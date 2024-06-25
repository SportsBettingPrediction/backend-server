from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save

from uuid import uuid4

# Model Schema
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
    
class WithdrawalRequest(models.Model):
    id = models.UUIDField(default=uuid4, primary_key=True, editable=False)
    transaction = models.OneToOneField(Transaction, on_delete=models.SET_NULL, related_name="withdrawal_request", null=True)
    account_number = models.CharField(max_length=20)
    account_name = models.CharField(max_length=50)
    bank_name = models.CharField(max_length=20)
    is_settled = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"WITHDRAWAL REQUEST: user ({self.transaction.user.email})\tamount ({self.transaction.amount})"
    
class DepositRequest(models.Model):
    id = models.UUIDField(default=uuid4, primary_key=True, editable=False)
    transaction = models.OneToOneField(Transaction, on_delete=models.SET_NULL, related_name="deposit_request", null=True)
    is_settled = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"DEPOSIT REQUEST: user ({self.transaction.user.email})\tamount ({self.transaction.amount})"
    

class Bet(models.Model):
    id = models.UUIDField(default=uuid4, primary_key=True, editable=False)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, related_name="user", null=True)
    game = models.CharField(max_length=20)
    amount = models.FloatField()
    status = models.CharField(max_length=20, choices=[("pending", "PENDING"), ("win", "WIN"), ("lose", "LOSE")])
    is_settled = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"BET: user ({self.user.email if self.user else ''})\tamount ({self.amount})"

# Model Signals
def update_transaction_balance(sender, instance, created, **kwargs):
    if instance.trans_type.lower() == "withdrawal":
        if instance.status.lower() != "pending" and not instance.withdrawal_request.is_settled:
            if instance.status.lower() == "successful" and not instance.withdrawal_request.is_settled:
                user_details = instance.user.user_details
                balance = user_details.balance
                user_details.balance = balance - instance.amount
                user_details.save()
                
            instance.withdrawal_request.is_settled = True
            instance.withdrawal_request.save()
            
    elif instance.trans_type.lower() == "deposit":
        if instance.status.lower() != "pending" and not instance.deposit_request.is_settled:
            if instance.status.lower() == "successful" and not instance.deposit_request.is_settled:
                user_details = instance.user.user_details
                balance = user_details.balance
                user_details.balance = balance + instance.amount
                user_details.save()
                
            instance.deposit_request.is_settled = True
            instance.deposit_request.save()

post_save.connect(update_transaction_balance, Transaction)

def update_bet_balance(sender, instance, created, **kwargs):
    if instance.status.lower() != "pending" and not instance.is_settled:
        if instance.status.lower() == "win" and not instance.is_settled:
            user_details = instance.user.user_details
            balance = user_details.balance
            user_details.balance = balance + instance.amount
            user_details.save()
            
        elif instance.status.lower() == "lose" and not instance.is_settled:
            user_details = instance.user.user_details
            balance = user_details.balance
            user_details.balance = balance - instance.amount
            user_details.save()
            
        instance.is_settled = True
        instance.save()
        
post_save.connect(update_bet_balance, Bet)