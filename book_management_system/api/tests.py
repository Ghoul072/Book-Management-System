from django.test import TestCase
from django.urls import reverse
from rest_framework import status

from .models import Book

# Create your tests here.

class BookAPITests(TestCase):
    def setUp(self) -> None:
        self.book = Book.objects.create(
            title = "ABC",
            author = "Author123",
            publicationYear = 2023,
            genre = "Test"
        )
        return super().setUp()
    
    def test_get_all_books(self):
        response = self.client.get(reverse('book-c'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_get_book_by_id(self):
        response = self.client.get(reverse('book-rud', kwargs={'pk': self.book.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'ABC')
        
    def test_create_book(self):
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
        response = self.client.delete(reverse('book-rud', kwargs={'pk': self.book.id}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Book.objects.count(), 0)
        