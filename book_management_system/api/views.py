from django.shortcuts import render

from rest_framework import generics
from .models import Book
from .serializers import BookSerializer
from rest_framework.pagination import PageNumberPagination


class BooksPagination(PageNumberPagination):
    page_size = 10  # Number of items per page
    page_size_query_param = 'page_size'
    max_page_size = 1000 

# Book Create view (the C in CRUD)
class BookCView(generics.ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    pagination_class = BooksPagination

# Book Read, Update, Delete view (RUD in CRUD)
class BookRUDView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
