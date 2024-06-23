from django.urls import path
from .views import LoginApiView, SignUpApiView, UpdateProfileImageView

urlpatterns = [
    path("login", LoginApiView.as_view()),
    path("signup", SignUpApiView.as_view()),
    path("profile_img", UpdateProfileImageView.as_view()),
]