from django.urls import path
from .views import LoginApiView, SignUpApiView

urlpatterns = [
    path("login", LoginApiView.as_view()),
    path("signup", SignUpApiView.as_view()),
]