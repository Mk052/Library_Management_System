from rest_framework import serializers

from lms.models import (User, Author, Category, Book)


class UserSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["id", "full_name", "email", "password"]

        def create(self, serializer):
            email = serializer.validated_data.get("email")
            password = self.request.data.get("password")

            # Check for missing or empty email
            if not email:
                raise serializer.ValidationError(
                    "Email is required and cannot be empty."
                )

            # Check for existing email before saving
            if User.objects.filter(email=email).exists():
                raise serializer.ValidationError(
                    "A user with this email already exists."
                )

            # Create and save the user securely
            student = serializer.save()
            student.set_password(password)
            student.save()

            return student


class AuthorSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()

    class Meta:
        model = Author
        fields = ["id", "name", "bio"]


class CategorySerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()

    class Meta:
        model = Category
        fields = ["id", "name"]


class BookSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    author_id = serializers.PrimaryKeyRelatedField(
        queryset=Author.objects.all(), write_only=True, source="author"
    )
    author = serializers.StringRelatedField(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), write_only=True, source="category"
    )
    category = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Book
        fields = [
            "id",
            "title",
            "description",
            "author",
            "category",
            "total_book",
            "book_copies",
            "author_id",
            "category_id",
        ]
