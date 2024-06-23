from django.urls import path
from .views import TransactionApiView

urlpatterns = [
    path("transaction", TransactionApiView.as_view()),
]