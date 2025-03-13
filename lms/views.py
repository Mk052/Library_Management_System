from rest_framework import generics, status
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from lms.models import (User, Student, Author, Category, Book)
from lms.serializers import (UserSerializer, AuthorSerializer,
                             CategorySerializer, BookSerializer)
from lms.utils import get_tokens_for_user


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
        Student.objects.create(user=user)


class UserLoginAPIView(generics.GenericAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        email = self.request.data.get("email")
        user = User.objects.filter(email=email).first()
        if not user:
            return Response({"msg": "User not found"})
        response = get_tokens_for_user(user)
        return Response(response)


class UserLogoutAPIView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        refresh_token = request.data.get("refresh_token")
        if refresh_token:
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"msg": "successfully logout"},
                            status=status.HTTP_200_OK)


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
    serializer_classes = AuthorSerializer
    permission_class = [IsAuthenticated]


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
