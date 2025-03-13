from django.urls import path

from lms.views import (UserRegistrationAPIView, UserLoginAPIView,
                       UserLogoutAPIView, UserListAPIView,
                       AuthorListCreateAPIView,
                       AuthorRetrieveUpdateDeleteAPIView,
                       CategoryListCreateAPIView, CategoryRetrieveUpdateDelete,
                       BookListCreateAPIView)

urlpatterns = [
    path("signup/", UserRegistrationAPIView.as_view()),
    path("login/", UserLoginAPIView.as_view()),
    path("logout/", UserLogoutAPIView.as_view()),
    path("user/", UserListAPIView.as_view()),
    path("author/", AuthorListCreateAPIView.as_view()),
    path("author/<int:pk>/", AuthorRetrieveUpdateDeleteAPIView.as_view()),
    path("category/", CategoryListCreateAPIView.as_view()),
    path("category/<int:pk>/", CategoryRetrieveUpdateDelete.as_view()),
    path("book/", BookListCreateAPIView.as_view()),
]
