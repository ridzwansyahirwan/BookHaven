from django.test import TestCase
from django.core.exceptions import ValidationError
from myapp.models import Book
from django.utils import timezone
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.auth.models import User 

#Test models.py
class BookModelTestCase(TestCase):

    #Test 1: testing valid years
    def test_valid_published_year(self):
        valid_years = [1200, 1957, 1999, timezone.now().year]
        for year in valid_years:
            book = Book(isbn='123-456-78901-234-5', title='Test Book', author='Test Author', published_year=year, genre='Test Genre')
            try:
                book.full_clean()  #Validate all fields
            except ValidationError as e:
                self.fail(f"Validation error for valid year {year}: {e}")

    #Test 2: testing invalid years
    def test_invalid_published_year(self):
        invalid_years = [-1, 999, timezone.now().year + 1]
        for year in invalid_years:
            book = Book(isbn='123-456-78901-234-5', title='Test Book', author='Test Author', published_year=year, genre='Test Genre')
            with self.assertRaises(ValidationError):
                book.full_clean() #this should be validation error
            
    #Test 3: testing invalid input (non integer)
    def test_non_integer_published_year(self):
        non_integer_year = 'invalid_year'
        book = Book(isbn='123-456-78901-234-5', title='Test Book', author='Test Author', published_year=non_integer_year, genre='Test Genre')
        with self.assertRaises(ValidationError):
            book.full_clean() #this should be validation error

    #Test 4: testing valid ISBN
    def test_valid_isbn(self):
        valid_isbns = ['123-456-78901-234-5', '987-654-32109-876-1']
        for isbn in valid_isbns:
            book = Book(isbn=isbn, title='Test Book', author='Test Author', published_year=2000, genre='Test Genre')
            try:
                book.full_clean()
            except ValidationError as e:
                self.fail(f"Validation error for valid ISBN {isbn}: {e}")

    #Test 5: testing invalid ISBN formats
    def test_invalid_isbn_format(self):
        invalid_isbns = ['123456789012345', '123-456-7890-123-5', 'abc-def-ghi-jkl-m']
        for isbn in invalid_isbns:
            book = Book(isbn=isbn, title='Test Book', author='Test Author', published_year=2000, genre='Test Genre')
            with self.assertRaises(ValidationError):
                book.full_clean()

    #Test 6: tetsing empty ISBN
    def test_empty_isbn(self):
        book = Book(title='Test Book', author='Test Author', published_year=2000, genre='Test Genre')
        with self.assertRaises(ValidationError):
            book.full_clean()


#Test views.py
class BookListAPIViewTestCase(TestCase):

    #setup test client
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='password123')   #user for testing
        self.client.login(username='testuser', password='password123') 
        self.book_data = {'isbn': '123-456-78901-234-5', 'title': 'Test Book', 'author': 'Test Author', 'published_year': 2023, 'genre': 'Test Genre'}
        self.url = reverse('book-list')

    def test_get_books(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_book(self):
        response = self.client.post(self.url, self.book_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 1)


class BookDetailAPIViewTestCase(TestCase):
    #setup test client
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='password123')  #user for testing
        self.client.login(username='testuser', password='password123')
        self.book = Book.objects.create(isbn='123-456-78901-234-5', title='Test Book', author='Test Author', published_year=2023, genre='Test Genre')
        self.url = reverse('book-detail', args=[self.book.pk])

    def test_get_book(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_book(self):
        updated_data = {'isbn': '123-456-78901-234-5', 'title': 'Updated Book Title', 'author': 'Updated Author', 'published_year': 2023, 'genre': 'Updated Genre'}
        response = self.client.put(self.url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book.refresh_from_db()
        self.assertEqual(self.book.title, 'Updated Book Title')

    def test_delete_book(self):
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Book.objects.filter(pk=self.book.pk).exists())


        