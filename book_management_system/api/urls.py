from django.urls import path, include
from . import views

urlpatterns = [
    path('books/', views.BookCView.as_view(), name='book-c'),               # POST: Add a new book
    path('books/<int:pk>/', views.BookRUDView.as_view(), name='book-rud'),  # GET, PUT, DELETE by ID
]