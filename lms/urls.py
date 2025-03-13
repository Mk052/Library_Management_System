from django.urls import path

from lms.views import (UserRegistrationAPIView, UserLoginAPIView,
                       UserLogoutAPIView, AuthorListCreateAPIView)

urlpatterns = [
    path("signup/", UserRegistrationAPIView.as_view()),
    path("login/", UserLoginAPIView.as_view()),
    path("logout/", UserLogoutAPIView.as_view()),
    path("author/", AuthorListCreateAPIView.as_view()),
]
