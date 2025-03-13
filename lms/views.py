from rest_framework import generics, status
from rest_framework.response import Response

from lms.models import (User, Student)
from lms.serializers import (UserSerializer)
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
