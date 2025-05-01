from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from lms.models import User, Author, Book, Category, Course, Student, IssueBook, Fine
from rest_framework_simplejwt.tokens import RefreshToken
from datetime import timedelta
from django.utils import timezone


class BaseTestSetup(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(email="admin@example.com", password="adminpass", is_staff=True)
        # self.admin_user = User.objects.create_superuser(email="u@example.com", password="adminpass", is_staff=True, is_superuser=True)
        self.student_user = User.objects.create_user(email="student@example.com", password="studentpass")
        self.student = Student.objects.create(user=self.student_user)
        self.token = RefreshToken.for_user(self.user).access_token
        self.auth_headers = {'HTTP_AUTHORIZATION': f'Bearer {self.token}'}


class UserAuthTests(BaseTestSetup):
    def test_user_registration(self):
        data = {
            "email": "testuser@example.com",
            "password": "testpass123",
            "full_name": "Test User"
        }
        response = self.client.post(reverse("user-register"), data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)



    def test_user_login(self):
        data = {"email": self.user.email, "password": "adminpass"}
        response = self.client.post(reverse("user-login"), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)

    def test_user_logout(self):
        refresh = RefreshToken.for_user(self.user)
        response = self.client.post(reverse("user-logout"), {"refresh_token": str(refresh)}, **self.auth_headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class AuthorTests(BaseTestSetup):
    def test_create_author(self):
        data = {"name": "Author One"}
        response = self.client.post(reverse("author-list"), data, **self.auth_headers)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_list_authors(self):
        Author.objects.create(name="Author A")
        response = self.client.get(reverse("author-list"), **self.auth_headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_update_delete_author(self):
        author = Author.objects.create(name="Author B")
        detail_url = reverse("author-detail", args=[author.id])
        res = self.client.get(detail_url, **self.auth_headers)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        res = self.client.put(detail_url, {"name": "Updated"}, **self.auth_headers)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        res = self.client.delete(detail_url, **self.auth_headers)
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)


class CategoryTests(BaseTestSetup):
    def test_category_crud(self):
        list_url = reverse("category-list")
        data = {"name": "Fiction"}
        response = self.client.post(list_url, data, **self.auth_headers)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        category_id = response.data["id"]
        detail_url = reverse("category-detail", args=[category_id])
        self.assertEqual(self.client.get(detail_url, **self.auth_headers).status_code, 200)
        self.assertEqual(self.client.put(detail_url, {"name": "Sci-Fi"}, **self.auth_headers).status_code, 200)
        self.assertEqual(self.client.delete(detail_url, **self.auth_headers).status_code, 204)


class BookTests(BaseTestSetup):
    def setUp(self):
        super().setUp()
        self.author = Author.objects.create(name="Author One")
        self.category = Category.objects.create(name="Category One")


    def test_create_list_book(self):
        # Create required related objects first
        author = Author.objects.create(name="Test Author")
        category = Category.objects.create(name="Fiction")

        # Book creation data
        book_data = {
            "title": "Test Book",
            "description": "Some description",
            "author_id": author.id,
            "category_id": category.id,
            "book_copies": 5
}


        # Authenticate as admin user
        self.admin_user = User.objects.create_superuser(email="user@example.com", password="userpass")
        self.client.force_authenticate(user=self.admin_user)

        # Create book
        response = self.client.post(reverse("book-list"), data=book_data)
        
        # Check for success
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Check that book appears in list
        list_response = self.client.get(reverse("book-list"))
        self.assertEqual(list_response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(list_response.data), 1)



class CourseTests(BaseTestSetup):
    def test_course_crud(self):
        list_url = reverse("course-list")
        data = {"name": "Django Basics"}
        response = self.client.post(list_url, data, **self.auth_headers)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        course_id = response.data["id"]
        detail_url = reverse("course-detail", args=[course_id])
        self.assertEqual(self.client.get(detail_url, **self.auth_headers).status_code, 200)
        self.assertEqual(self.client.put(detail_url, {"name": "Advanced Django"}, **self.auth_headers).status_code, 200)
        self.assertEqual(self.client.delete(detail_url, **self.auth_headers).status_code, 204)


class IssueBookTests(BaseTestSetup):
    def setUp(self):
        super().setUp()
        self.author = Author.objects.create(name="Author")
        self.category = Category.objects.create(name="Category")
        self.book = Book.objects.create(title="Book", description="desc", book_copies=1, author=self.author, category=self.category)


    def test_issue_book(self):
        # Make sure the book has available copies
        self.book.book_copies = 1
        self.book.save()

        # Use timezone-aware datetime
        issue_date = timezone.now()
        return_date = issue_date + timedelta(days=7)

        data = {
            "book_id": self.book.id,
            "student_id": self.student.id,
            "issue_date": issue_date.isoformat(),
            "return_date": return_date.isoformat()
        }


        response = self.client.post(
            reverse("issue-book-list"),
            data,
            format="json",
            **self.auth_headers
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

class BookReturnTests(BaseTestSetup):
    def setUp(self):
        super().setUp()
        self.author = Author.objects.create(name="Author")
        self.category = Category.objects.create(name="Category")
        self.book = Book.objects.create(title="Book", description="desc", book_copies=0, author=self.author, category=self.category)
        self.issue_book = IssueBook.objects.create(book=self.book, student=self.student)

    def test_return_book(self):
        url = reverse("book-return", args=[self.issue_book.id])
        response = self.client.patch(url, **self.auth_headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class FineTests(BaseTestSetup):
    def setUp(self):
        super().setUp()
        self.author = Author.objects.create(name="Author")
        self.category = Category.objects.create(name="Category")
        self.book = Book.objects.create(title="Book", description="desc", book_copies=1, author=self.author, category=self.category)
        self.issue_book = IssueBook.objects.create(book=self.book, student=self.student, return_date=timezone.now() - timedelta(days=5))

    def test_create_fine(self):
        data = {"issue_book_id": self.issue_book.id, "amount": 50, "reason": "Late return"}
        response = self.client.post(reverse("fine-list-create"), data, **self.auth_headers)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_fine_list_by_student(self):
        Fine.objects.create(issue_book=self.issue_book, amount=50)
        url = reverse("student-fines", args=[self.student.id])
        response = self.client.get(url, **self.auth_headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class SearchTests(BaseTestSetup):
    def test_search_books(self):
        Book.objects.create(title="Python 101", description="Basics", book_copies=1, author=Author.objects.create(name="A1"), category=Category.objects.create(name="C1"))
        url = reverse("search") + "?s=Python"
        response = self.client.get(url, **self.auth_headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
















