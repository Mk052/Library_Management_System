from rest_framework import serializers

from lms.models import Author, Book, Category, Course, Fine, IssueBook, Student, User


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


class CourseSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()

    class Meta:
        model = Course
        fields = ["id", "name"]


class StudentSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    course_id = serializers.PrimaryKeyRelatedField(
        queryset=Course.objects.all(), write_only=True, source="course"
    )
    course = serializers.StringRelatedField(read_only=True)
    user_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), write_only=True, source="user"
    )
    user = serializers.StringRelatedField(read_only=True, source="__str__")

    class Meta:
        model = Student
        fields = ["id", "user", "roll_no", "course", "course_id", "user_id"]


class IssueBookSerializer(serializers.ModelSerializer):
    student = serializers.StringRelatedField(read_only=True)
    student_id = serializers.PrimaryKeyRelatedField(
        queryset=Student.objects.all(), write_only=True, source="student"
    )
    book = serializers.StringRelatedField(read_only=True)
    book_id = serializers.PrimaryKeyRelatedField(
        queryset=Book.objects.all(), write_only=True, source="book"
    )

    class Meta:
        model = IssueBook
        fields = [
            "id",
            "book",
            "student",
            "issue_date",
            "return_date",
            "is_returned",
            "student_id",
            "book_id",
        ]


class FineSerializer(serializers.ModelSerializer):
    issue_book_id = serializers.PrimaryKeyRelatedField(
        queryset=IssueBook.objects.all(), write_only=True, source="issue_book"
    )
    issue_book = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Fine
        fields = ["id", "issue_book", "amount", "paid", "issue_book_id"]
