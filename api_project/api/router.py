from django.urls import path, include
from .views import BookList, BookViewSet
from rest_framework.routers import DefaultRouter

class CustomRouter(DefaultRouter):
    """
    Custom router to handle API endpoints for BookViewSet.
    """
    def __init__(self):
        super().__init__()
        self.register(r'books_all', BookViewSet, basename='book_all')   
