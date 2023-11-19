from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from . import views

urlpatterns = [
    path('books/', views.BookCView.as_view(), name='book-c'),               # POST: Add a new book
    path('books/<int:pk>/', views.BookRUDView.as_view(), name='book-rud'),  # GET, PUT, DELETE by ID
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]