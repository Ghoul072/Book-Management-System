from django.db import models

# Create your models here.
    
class Book:
    id = models.AutoField(primary_key=True)  # Auto-incrementing integer ID
    title = models.CharField(max_length=255)  # String field for the title
    author = models.CharField(max_length=255)  # String field for the author's name
    publicationYear = models.IntegerField()  # Integer field for publication year
    genre = models.CharField(max_length=100)  # String field for the genre
    
    def __str__(self):
        return self.title  # Display the title of the book in admin or shell

    class Meta:
        verbose_name = "Book"
        verbose_name_plural = "Books"