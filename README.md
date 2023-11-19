# Book Management System

Simple CRUD API for a book management system using Django

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
```js
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
        // Other book details...
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
