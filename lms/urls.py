from django.urls import path

from lms.views import (UserRegistrationAPIView)

urlpatterns = [
    path("signup/", UserRegistrationAPIView.as_view()),
]
