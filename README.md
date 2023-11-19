# Book Management System

Simple CRUD API for a book management system using Django

## Setup Guide

### Prerequisites
Ensure you have the following installed:
- Python (Python 3.x)
- Pip (Python package installer)
- Git (version control system)

### Setup Steps

1. **Clone the Project Repository:**
    ```bash
    git clone <repository_url>
    cd <project_directory>
    ```

2. **Create a Virtual Environment (Optional but Recommended):**
    ```bash
    python -m venv venv_name
    ```
    
3. Activate the virtual environment:
    ```
    # On Windows
    venv_name\Scripts\activate
    
    # On macOS / Linux
    source venv_name/bin/activate
    ```

4. **Install Project Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

5. **Database Setup (Assuming SQLite for simplicity):**
    ```bash
    python manage.py migrate
    ```
    
6. **Navigate to the `book_management_system` folder**
   ```bash
    cd book_management_system
    ```
   
7. **Create Superuser (For Django Admin Access):**
    ```bash
    python manage.py createsuperuser
    # Follow the prompt to set username, email, and password
    ```

8. **Run Tests:**
    ```bash
    python manage.py test
    ```

9. **Run the Django Development Server:**
    ```bash
    python manage.py runserver
    ```

10. **Access the Application:**
    Open a web browser and go to `http://127.0.0.1:8000/` to view your application.
    - Use the `/admin/` route to access the Django admin panel and log in with the superuser credentials you created.
    - Use the below API Guide to make use of the Book Management API


# Book Management API

## Authentication

This API uses JSON Web Token (JWT) authentication. To authenticate and receive a token, use the following endpoints:

- `POST /token/`: Obtain a JWT token by providing valid credentials (username and password).
- `POST /token/refresh/`: Refresh the JWT token by providing a valid refresh token.

## Endpoints

### Books

#### Get All Books
- **URL:** `/books/`
- **Method:** `GET`
- **Description:** Retrieve a paginated list of all books.
- **Authentication:** Token-based authentication required.
- **Request Parameters:**
    - `page`: Page number for pagination (default is 1).
- **Response:** Returns a paginated list of books.

*Example:*

**Request (Curl):**
```bash
curl -X GET http://yourapi.com/books/?page=1
```

**Response (200 OK - JSON):**
```json
{
    "count": 10,
    "next": "http://yourapi.com/books/?page=2",
    "previous": null,
    "results": [
        {
            "id": 1,
            "title": "Book Title 1",
            "author": "Author Name",
            "publicationYear": 2005,
            "genre": "Fiction"
        },
        {
            "id": 2,
            "title": "Yet Another Book, and so on",
            "author": "Author Name",
            "publicationYear": 2020,
            "genre": "Fiction"
        },
    ]
}
```

#### Add a New Book
- **URL:** `/books/`
- **Method:** `POST`
- **Description:** Add a new book to the library.
- **Authentication:** Token-based authentication required.
- **Request Body (JSON):** 
    ```json
    {
        "title": "New Book Title",
        "author": "New Author",
        "publicationYear": 2022,
        "genre": "Sci-Fi"
    }
    ```
- **Response:** Returns the details of the newly created book.

*Example:*

**Request (Curl):**
```bash
curl -X POST -H "Authorization: Bearer <token>" -d '{"title": "New Book Title", "author": "New Author", "publicationYear": 2022, "genre": "Sci-Fi"}' -H "Content-Type: application/json" http://yourapi.com/books/
```

**Response (201 Created - JSON):**
```json
{
    "id": 101,
    "title": "New Book Title",
    "author": "New Author",
    "publicationYear": 2022,
    "genre": "Sci-Fi"
}
```

#### Get a Book by ID
- **URL:** `/books/<int:pk>/`
- **Method:** `GET`
- **Description:** Retrieve details of a specific book by its ID.
- **Authentication:** Token-based authentication required.
- **Response:** Returns details of the book.

*Example:*

**Request (Curl):**
```bash
curl -X GET http://yourapi.com/books/1/
```

**Response (200 OK - JSON):**
```json
{
    "id": 1,
    "title": "Book Title 1",
    "author": "Author Name",
    "publicationYear": 2005,
    "genre": "Fiction"
}
```

#### Update a Book by ID
- **URL:** `/books/<int:pk>/`
- **Method:** `PUT`
- **Description:** Update details of a specific book by its ID.
- **Authentication:** Token-based authentication required.
- **Request Body (JSON):** 
    ```json
    {
        "title": "Updated Book Title",
        "author": "Updated Author",
        "publicationYear": 2023,
        "genre": "Updated Genre"
    }
    ```
- **Response:** Returns details of the updated book.

*Example:*

**Request (Curl):**
```bash
curl -X PUT -H "Authorization: Bearer <token>" -d '{"title": "Updated Book Title", "author": "Updated Author", "publicationYear": 2023, "genre": "Updated Genre"}' -H "Content-Type: application/json" http://yourapi.com/books/1/
```

**Response (200 OK - JSON):**
```json
{
    "id": 1,
    "title": "Updated Book Title",
    "author": "Updated Author",
    "publicationYear": 2023,
    "genre": "Updated Genre"
}
```

#### Delete a Book by ID
- **URL:** `/books/<int:pk>/`
- **Method:** `DELETE`
- **Description:** Delete a specific book by its ID.
- **Authentication:** Token-based authentication required.
- **Response:** Returns a success message on deletion.

*Example:*

**Request (Curl):**
```bash
curl -X DELETE -H "Authorization: Bearer <token>" http://yourapi.com/books/1/
```

**Response (204 No Content):**
```
No content returned for a successful deletion.
```
