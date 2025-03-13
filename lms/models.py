from django.contrib.auth.models import AbstractUser
from django.db import models

from lms.managers import CustomUserManager


# Timestamped Model for Auto-Created/Updated Fields
class TimestampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


# Category Model
class Category(TimestampedModel):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


# Author Model
class Author(TimestampedModel):
    name = models.CharField(max_length=100)
    bio = models.CharField(max_length=225, blank=True)

    def __str__(self):
        return self.name


# Book Model
class Book(TimestampedModel):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    author = models.ForeignKey(
        Author, on_delete=models.CASCADE, related_name="books", blank=True
    )
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="books"
    )
    total_book = models.PositiveIntegerField(default=1)
    book_copies = models.PositiveIntegerField(default=1)

    def __str__(self):
        return self.title


# Course Model
class Course(TimestampedModel):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


# User Model (Replaces the old Student model)
class User(AbstractUser, TimestampedModel):
    username = None  # Remove username field from AbstractUser
    full_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email


# New Student Model with One-to-One Relationship to User
class Student(TimestampedModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="student")
    roll_no = models.PositiveIntegerField(unique=True, null=True, blank=True)
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.user.email


# IssueBook Model with Updated Relationship to Student Model
class IssueBook(TimestampedModel):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="issue_books")
    student = models.ForeignKey(
        Student, on_delete=models.CASCADE, related_name="issue_books", blank=True
    )
    issue_date = models.DateTimeField(auto_now_add=True)
    return_date = models.DateTimeField(null=True, blank=True)
    is_returned = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.book.title} issued to {self.student.user.email}"


# Fine Model
class Fine(TimestampedModel):
    issue_book = models.ForeignKey(
        IssueBook, on_delete=models.CASCADE, related_name="fines"
    )
    amount = models.PositiveIntegerField()
    paid = models.BooleanField(default=False)

    def __str__(self):
        return f"Fine for {self.issue_book.book.title} - Amount: {self.amount}"
