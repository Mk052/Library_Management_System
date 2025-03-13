from django.urls import path

from lms.views import (UserRegistrationAPIView, UserLoginAPIView)

urlpatterns = [
    path("signup/", UserRegistrationAPIView.as_view()),
    path("login/", UserLoginAPIView.as_view()),
]
