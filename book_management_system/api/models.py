from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from datetime import datetime as dt
    
class Book(models.Model):
    id = models.AutoField(primary_key=True)     # Auto-incrementing integer ID
    title = models.CharField(max_length=255)    # String field for the title
    author = models.CharField(max_length=255)   # String field for the author's name
    publicationYear = models.IntegerField(      # Integer field for publication year
        validators=[
            MinValueValidator(1, message="Publication year cannot be less than 1"), # Assuming books were not published in BC time periods. This can be edited to accomodate BC years
            MaxValueValidator(dt.today().year, message="Publication year cannot be in the future")
        ],
        null=True, blank=True # In the case where publication year is unknown, allow to leave this field blank
        ) 
    genre = models.CharField(max_length=100)  # String field for the genre
    
    def __str__(self):
        return self.title  # Display the title of the book in admin or shell

    class Meta:
        verbose_name = "Book"
        verbose_name_plural = "Books"