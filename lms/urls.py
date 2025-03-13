from django.urls import path

from lms.views import (UserRegistrationAPIView, UserLoginAPIView,
                       UserLogoutAPIView, UserListAPIView,
                       AuthorListCreateAPIView,
                       AuthorRetrieveUpdateDeleteAPIView,
                       CategoryListCreateAPIView, CategoryRetrieveUpdateDelete,
                       BookListCreateAPIView, BookRetrieveUpdateDeleteAPIView,
                       CourseListCreateAPIView, CourseRetrieveUpdateDelete,
                       StudentListAPIView, StudentRetrieveUpdateDelete,
                       IssueBookListCreateAPIView, BookReturnUpdateAPIView,
                       FineListCreateAPIView, FineRetrieveUpdateDeleteAPIView)

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
    path("book/<int:pk>/", BookRetrieveUpdateDeleteAPIView.as_view()),
    path("course/", CourseListCreateAPIView.as_view()),
    path("course/<int:pk>/", CourseRetrieveUpdateDelete.as_view()),
    path("student/", StudentListAPIView.as_view()),
    path("student/<int:pk>/", StudentRetrieveUpdateDelete.as_view()),
    path("issuebook/", IssueBookListCreateAPIView.as_view()),
    path("returnbook/<int:pk>/", BookReturnUpdateAPIView.as_view()),
    path("fine/", FineListCreateAPIView.as_view()),
    path("fine/<int:pk>/", FineRetrieveUpdateDeleteAPIView.as_view()),
]
