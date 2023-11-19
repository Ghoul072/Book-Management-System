from rest_framework import serializers
from django.core.validators import MinValueValidator
from datetime import datetime as dt
from .models import Book

class BookSerializer(serializers.ModelSerializer):
    
    # Validation for required fields
    title = serializers.CharField(required=True)
    author = serializers.CharField(required=True)
    
    
    class Meta:
        model = Book
        fields = ('id', 'title', 'author', 'publicationYear', 'genre')
        
    def validate_publicationYear(self, value):
        if value > dt.now().year:
            raise serializers.ValidationError("Publication year cannot be in the future.")
        return value