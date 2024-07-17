from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Transaction)
admin.site.register(AdminAccountDetails)
admin.site.register(WithdrawalRequest)
admin.site.register(DepositRequest)
admin.site.register(Bet)