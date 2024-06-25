from django.urls import path
from .views import TransactionApiView, BetHistoryApiView, WithdrawalApiView, DepositApiView

urlpatterns = [
    path("transactions", TransactionApiView.as_view()),
    path("bets_history", BetHistoryApiView.as_view()),
    path("withdraw", WithdrawalApiView.as_view()),
    path("deposit", DepositApiView.as_view()),
]