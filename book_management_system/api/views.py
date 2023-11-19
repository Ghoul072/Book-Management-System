from django.shortcuts import render

from rest_framework import generics
from .models import Book
from .serializers import BookSerializer

# Create your views here.

# Book Create view (the C in CRUD)
class BookCView(generics.ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

# Book Read, Update, Delete view (RUD in CRUD)
class BookRUDView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
