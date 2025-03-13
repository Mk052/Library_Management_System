from django.urls import path

from lms.views import (UserRegistrationAPIView, UserLoginAPIView,
                       UserLogoutAPIView)

urlpatterns = [
    path("signup/", UserRegistrationAPIView.as_view()),
    path("login/", UserLoginAPIView.as_view()),
    path("logout/", UserLogoutAPIView.as_view()),
]
