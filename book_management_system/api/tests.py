from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from datetime import datetime as dt

from .models import Book
from .serializers import BookSerializer

class BookAPITests(TestCase):
    def setUp(self) -> None:
        # Create a book instance for testing
        self.book = Book.objects.create(
            title="ABC",
            author="Author123",
            publicationYear=2023,
            genre="Test"
        )
        return super().setUp()
    
    def test_get_all_books(self):
        # Test retrieving all books
        response = self.client.get(reverse('book-c'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_get_book_by_id(self):
        # Test retrieving a specific book by its ID
        response = self.client.get(reverse('book-rud', kwargs={'pk': self.book.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'ABC')
        
    def test_create_book(self):
        # Test creating a new book
        data = {
            "title": "DEF",
            "author": "Author456",
            "publicationYear": 2023,
            "genre": "Test"
        }
        response = self.client.post(reverse('book-c'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 2)
        
    def test_delete_book(self):
        # Test deleting a book
        response = self.client.delete(reverse('book-rud', kwargs={'pk': self.book.id}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Book.objects.count(), 0)
        
    def test_publication_year_validation(self):
        current_year = dt.now().year

        # Test publication year validation:
        # Check with current year
        valid_data = {
            'title': 'Test Book',
            'author': 'Test Author',
            'publicationYear': current_year,
            'genre': 'Test Genre'
        }
        response = self.client.post(reverse('book-c'), valid_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 2)
        
        # Check with past year
        valid_data = {
            'title': 'Test Book',
            'author': 'Test Author',
            'publicationYear': current_year - 1,
            'genre': 'Test Genre'
        }
        response = self.client.post(reverse('book-c'), valid_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 3)
        
        # Check with future year. This should raise an error
        valid_data = {
            'title': 'Test Book',
            'author': 'Test Author',
            'publicationYear': current_year + 1,
            'genre': 'Test Genre'
        }
        response = self.client.post(reverse('book-c'), valid_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST) # Bad Request as date is in the future
        self.assertEqual(Book.objects.count(), 3) # No new books added
