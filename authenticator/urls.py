from django.urls import path
from .views import LoginApiView, SignUpApiView, UpdateProfileImageView, UpdatePasswordApiView, UpdatePhoneNumberApiView

urlpatterns = [
    path("login", LoginApiView.as_view()),
    path("signup", SignUpApiView.as_view()),
    path("update_profile_img", UpdateProfileImageView.as_view()),
    path("update_password", UpdatePasswordApiView.as_view()),
    path("update_phonenumber", UpdatePhoneNumberApiView.as_view()),
]