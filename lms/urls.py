from django.urls import path

from lms.views import (UserRegistrationAPIView, UserLoginAPIView,
                       UserLogoutAPIView, AuthorListCreateAPIView,
                       AuthorRetrieveUpdateDeleteAPIView)

urlpatterns = [
    path("signup/", UserRegistrationAPIView.as_view()),
    path("login/", UserLoginAPIView.as_view()),
    path("logout/", UserLogoutAPIView.as_view()),
    path("author/", AuthorListCreateAPIView.as_view()),
    path("author/<int:pk>/", AuthorRetrieveUpdateDeleteAPIView.as_view()),
]
