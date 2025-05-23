from datetime import datetime

from django.utils import timezone
from rest_framework import generics, status
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from lms.models import Author, Book, Category, Course, Fine, IssueBook, Student, User
from lms.permission import BookReturnPermission, CustomPermission
from lms.serializers import (
    AuthorSerializer,
    BookSerializer,
    CategorySerializer,
    CourseSerializer,
    FineSerializer,
    IssueBookSerializer,
    StudentSerializer,
    UserSerializer,
)
from lms.utils import get_tokens_for_user
from rest_framework import serializers


class UserRegistrationAPIView(generics.GenericAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):

        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            self.perform_create(serializer)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def perform_create(self, serializer):
        user = serializer.save()
        user.set_password(serializer.validated_data["password"])
        user.save()
        Student.objects.create(user=user)


class UserLoginAPIView(generics.GenericAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        email = self.request.data.get("email")
        password = self.request.data.get("password")
        user = User.objects.filter(email=email).first()
        if not user:
            return Response({"msg": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        if user.check_password(password):
            response = get_tokens_for_user(user)
            return Response(response)
        else:
            return Response({"msg": "password incorrect"})


class UserLogoutAPIView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        refresh_token = request.data.get("refresh_token")
        if refresh_token:
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"msg": "successfully logout"}, status=status.HTTP_200_OK)


class UserListAPIView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class AuthorListCreateAPIView(generics.ListCreateAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = PageNumberPagination


class AuthorRetrieveUpdateDeleteAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [IsAuthenticated]


class CategoryListCreateAPIView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]
    pagination_class = PageNumberPagination


class CategoryRetrieveUpdateDelete(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]


class BookListCreateAPIView(generics.ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    pagination_class = PageNumberPagination

    def get_permissions(self):
        if self.request.method in ["POST"]:
            return [IsAdminUser(), IsAuthenticated()]
        return [IsAuthenticated()]

    def get_queryset(self):
        author = self.request.GET.get("author")
        category = self.request.GET.get("category")
        book = Book.objects.all()
        if author:
            book = book.filter(author__name=author)
        if category:
            book = book.filter(category__name=category)
        return book


class BookRetrieveUpdateDeleteAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAdminUser]


class CourseListCreateAPIView(generics.ListCreateAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = PageNumberPagination


class CourseRetrieveUpdateDelete(generics.RetrieveUpdateDestroyAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated]


class StudentListAPIView(generics.ListAPIView):
    serializer_class = StudentSerializer
    permission_classes = [IsAuthenticated, CustomPermission]
    pagination_class = PageNumberPagination
    queryset = Student.objects.all()


class StudentRetrieveUpdateDelete(generics.RetrieveUpdateDestroyAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = [IsAuthenticated, CustomPermission]


# class IssueBookListCreateAPIView(generics.ListCreateAPIView):
#     queryset = IssueBook.objects.all()
#     serializer_class = IssueBookSerializer
#     permission_classes = [IsAuthenticated]
#     pagination_class = PageNumberPagination

#     def post(self, request, *args, **kwargs):
#         book_id = request.data.get("book_id")
#         # breakpoint()
#         # student_id = self.request.data.get('student_id')
#         book = Book.objects.filter(id=book_id).first()
#         # if not Student.objects.filter(id=student_id).first():
#         #     return Response({"msg": "student does not exist"}, status=status.HTTP_404_NOT_FOUND)
#         if not book:
#             return Response(
#                 {"msg": "book does not exist"}, status=status.HTTP_404_NOT_FOUND
#             )
#         if book.book_copies < 1:
#             return Response({"msg": "book is not available"})
#         book.book_copies -= 1
#         book.save()
#         serializer = self.serializer_class(data=request.data)

#         if serializer.is_valid(raise_exception=True):
#             serializer.save()

#         return Response(serializer.data)

#     def get_queryset(self):
#         student = self.request.GET.get("student")
#         book = self.request.GET.get("book")
#         issue_book = IssueBook.objects.all()
#         if student:
#             # issue_book = issue_book.filter(student__id=student)
#             issue_book = issue_book.filter(student__user__email=student)
#         if book:
#             issue_book = issue_book.filter(book__id=book)
#             # issue_book = issue_book.filter(book__title__icontains=book)
#         return issue_book
class IssueBookListCreateAPIView(generics.ListCreateAPIView):
    queryset = IssueBook.objects.all()
    serializer_class = IssueBookSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = PageNumberPagination

    def perform_create(self, serializer):
        book = serializer.validated_data["book"]
        if book.book_copies < 1:
            raise serializers.ValidationError({"msg": "book is not available"})
        book.book_copies -= 1
        book.save()
        serializer.save()

    def get_queryset(self):
        student = self.request.GET.get("student")
        book = self.request.GET.get("book")
        issue_book = IssueBook.objects.all()
        if student:
            issue_book = issue_book.filter(student__user__email=student)
        if book:
            issue_book = issue_book.filter(book__id=book)
        return issue_book



class BookReturnUpdateAPIView(generics.UpdateAPIView):
    queryset = IssueBook.objects.all()
    serializer_class = IssueBookSerializer
    permission_classes = [IsAuthenticated, BookReturnPermission]

    def patch(self, request, *args, **kwargs):
        issue_book = IssueBook.objects.filter(id=self.kwargs.get("pk")).first()
        if issue_book is None:
            return Response(
                {"msg": "Issued book does not exit"}, status=status.HTTP_404_NOT_FOUND
            )
        if issue_book.is_returned:
            return Response(
                {"msg": "This book is already returned"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        book = issue_book.book
        book.book_copies += 1
        book.save()
        issue_book.return_date = timezone.now()
        issue_book.is_returned = True
        issue_book.save()
        serializer = self.serializer_class(issue_book)
        return Response(serializer.data)


class FineListCreateAPIView(generics.ListCreateAPIView):
    queryset = Fine.objects.all()
    serializer_class = FineSerializer
    pagination_class = PageNumberPagination
    permission_classes = [IsAuthenticated]

    def post(self, request):
        issue_book_id = request.data.get("issue_book_id")
        issue_book = IssueBook.objects.filter(id=issue_book_id).first()

        if issue_book is None:
            return Response(
                {"msg": "issue book does not exist"}, status=status.HTTP_404_NOT_FOUND
            )

        if not issue_book.is_returned and issue_book.return_date and issue_book.return_date < timezone.now():
            serializer = self.serializer_class(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(
            {"msg": "book already returned within time period or return_date not set"},
            status=status.HTTP_400_BAD_REQUEST,
        )


class FineRetrieveUpdateDeleteAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Fine.objects.all()
    serializer_class = FineSerializer
    permission_classes = [IsAuthenticated]


class FineStudentListAPIView(generics.ListAPIView):
    def get(self, request, **kwargs):
        student_id = self.kwargs.get("pk")
        student = Student.objects.filter(id=student_id).first()
        if not student:
            return Response(
                {"msg": "student does not exits"}, status=status.HTTP_404_NOT_FOUND
            )
        fine = Fine.objects.filter(issue_book__student=student)
        serializer = FineSerializer(fine, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class SearchAPIView(generics.ListAPIView):
    def get(self, request):
        search_query = request.GET.get("s")
        if not search_query:
            return Response({"msg": "provide the search value"})
        book = Book.objects.filter(title__icontains=search_query)
        if book:
            serializer = BookSerializer(book, many=True)
            return Response(serializer.data)
        author = Author.objects.filter(name__icontains=search_query)
        if author:
            serializer = AuthorSerializer(author, many=True)
            return Response(serializer.data)
        category = Category.objects.filter(name__icontains=search_query)
        if category:
            serializer = CategorySerializer(category, many=True)
            return Response(serializer.data)

        return Response({"msg": "No results found"}, status=status.HTTP_404_NOT_FOUND)
