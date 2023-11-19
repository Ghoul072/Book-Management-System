from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

from rest_framework import status
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import AccessToken

from datetime import datetime as dt

from .models import Book


class AuthenticationTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_unauthenticated_request(self):
        # Make an unauthenticated request to the endpoint
        response = self.client.get(reverse('book-c'))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
    def test_authentication(self):
        # Create a user
        user = User.objects.create_user(username='testuser', password='testpassword')
        # Authenticate and get JWT token
        response = self.client.post(
            reverse('token_obtain_pair'),
            {'username': "testuser", 'password': "testpassword"},
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

        access_token = response.data['access']

        # Use the obtained token for authenticated requests
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')

        # Make an authenticated request to the endpoint
        response = self.client.get(reverse('book-c'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class BookAPITests(TestCase):
    def setUp(self) -> None:
        
        self.client = APIClient()
        user = User.objects.create_user(username='testuser', password='testpassword')   # Create a test user
        access_token = AccessToken.for_user(user)                                       # Generate an access token for the user
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')            # Set the token in the HTTP header
        
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
        
    def test_update_book(self):
        # Create a book to update
        book = Book.objects.create(
            title="Original Title",
            author="Original Author",
            publicationYear=2023,
            genre="Test"
        )

        # Data for updating the book
        update_data = {
            "title": "Updated Title",
            "author": "Updated Author",
            "publicationYear": 2019,
            "genre": "Updated Genre"
        }

        # Test updating the book details via PUT request
        response = self.client.put(reverse('book-rud', kwargs={'pk': book.id}), update_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Retrieve the updated book from the database
        updated_book = Book.objects.get(id=book.id)

        # Verify that the book details are updated as expected
        self.assertEqual(updated_book.title, "Updated Title")
        self.assertEqual(updated_book.author, "Updated Author")
        self.assertEqual(updated_book.publicationYear, 2019)
        self.assertEqual(updated_book.genre, "Updated Genre")
        
    def test_update_invalid_book(self):
        # Test updating a book with invalid information
        data = {
            'publicationYear': -1,  # Invalid publication year
        }
        url = reverse('book-rud', kwargs={'pk': self.book.id})
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
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
        
    def test_create_book_missing_title(self):
        # Test creating a book without providing a title
        data = {
            "author": "Author456",
            "publicationYear": 2023,
            "genre": "Test"
        }
        response = self.client.post(reverse('book-c'), data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Book.objects.count(), 1)  # No new book should be added
        
    def test_create_book_missing_author(self):
        # Test creating a book without providing an author
        data = {
            "title": "DEF",
            "publicationYear": 2023,
            "genre": "Test"
        }
        response = self.client.post(reverse('book-c'), data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Book.objects.count(), 1)  # No new books should be added
        

class Pagination_Test(TestCase):
    def setUp(self):
        
        self.client = APIClient()
        user = User.objects.create_user(username='testuser', password='testpassword')   # Create a test user
        access_token = AccessToken.for_user(user)                                       # Generate an access token for the user
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')            # Set the token in the HTTP header
        
        # Create 15 books for testing pagination
        for i in range(15):
            Book.objects.create(
                title=f"Book {i}",
                author=f"Author {i}",
                publicationYear=2000 + i,
                genre="Test Genre"
            )

    def test_pagination_structure(self):
        response = self.client.get(reverse('book-c'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check the structure of the paginated response
        self.assertIn('results', response.data)
        self.assertIn('count', response.data)
        self.assertIn('next', response.data)
        self.assertIn('previous', response.data)

        # Verify the number of items per page
        self.assertEqual(len(response.data['results']), 10)  # Page size is set to 10

    def test_pagination_next_page(self):
        response = self.client.get(reverse('book-c'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        next_page_url = response.data['next']
        self.assertIsNotNone(next_page_url)

        # Access the next page
        next_page_response = self.client.get(next_page_url)
        self.assertEqual(next_page_response.status_code, status.HTTP_200_OK)

        # Verify that the next page contains the remaining items
        self.assertEqual(len(next_page_response.data['results']), 5)  # Remaining items (15 total books)
