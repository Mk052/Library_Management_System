from django.urls import path

from lms.views import (
    AuthorListCreateAPIView,
    AuthorRetrieveUpdateDeleteAPIView,
    BookListCreateAPIView,
    BookRetrieveUpdateDeleteAPIView,
    BookReturnUpdateAPIView,
    CategoryListCreateAPIView,
    CategoryRetrieveUpdateDelete,
    CourseListCreateAPIView,
    CourseRetrieveUpdateDelete,
    FineListCreateAPIView,
    FineRetrieveUpdateDeleteAPIView,
    FineStudentListAPIView,
    IssueBookListCreateAPIView,
    SearchAPIView,
    StudentListAPIView,
    StudentRetrieveUpdateDelete,
    UserListAPIView,
    UserLoginAPIView,
    UserLogoutAPIView,
    UserRegistrationAPIView,
)

urlpatterns = [
    path("signup/", UserRegistrationAPIView.as_view(), name="user-register"),
    path("login/", UserLoginAPIView.as_view(), name="user-login"),
    path("logout/", UserLogoutAPIView.as_view(), name="user-logout"),
    path("user/", UserListAPIView.as_view(), name="user-list"),
    path("author/", AuthorListCreateAPIView.as_view(), name="author-list"),
    path(
        "author/<int:pk>/",
        AuthorRetrieveUpdateDeleteAPIView.as_view(),
        name="author-detail",
    ),
    path("category/", CategoryListCreateAPIView.as_view(), name="category-list"),
    path(
        "category/<int:pk>/",
        CategoryRetrieveUpdateDelete.as_view(),
        name="category-detail",
    ),
    path("book/", BookListCreateAPIView.as_view(), name="book-list"),
    path(
        "book/<int:pk>/", BookRetrieveUpdateDeleteAPIView.as_view(), name="book-detail"
    ),
    path("course/", CourseListCreateAPIView.as_view(), name="course-list"),
    path(
        "course/<int:pk>/", CourseRetrieveUpdateDelete.as_view(), name="course-detail"
    ),
    path("student/", StudentListAPIView.as_view(), name="student-list"),
    path(
        "student/<int:pk>/",
        StudentRetrieveUpdateDelete.as_view(),
        name="student-detail",
    ),
    path("issuebook/", IssueBookListCreateAPIView.as_view(), name="issue-book-list"),
    path("returnbook/<int:pk>/", BookReturnUpdateAPIView.as_view(), name="book-return"),
    path("fine/", FineListCreateAPIView.as_view(), name="fine-list-create"),
    path(
        "fine/<int:pk>/", FineRetrieveUpdateDeleteAPIView.as_view(), name="fine-detail"
    ),
    path(
        "fine/student/<int:pk>/", FineStudentListAPIView.as_view(), name="student-fines"
    ),
    path("search/", SearchAPIView.as_view(), name="search"),
]
