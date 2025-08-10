from django.shortcuts import render
from rest_framework import viewsets
from .models import Author, Book
from .serializers import AuthorSerializer, BookSerializer
from rest_framework import generics, permissions
from .permissions import IsOwnerOrReadOnly




# -----------------------------
# LIST VIEW (Read-only)
# -----------------------------
class BookListView(generics.ListAPIView):
    """
    Handles GET requests to retrieve a list of all Book instances.
    - Accessible to everyone (no authentication required).
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]  # Public read access


# -----------------------------
# DETAIL VIEW (Read-only)
# -----------------------------
class BookDetailView(generics.RetrieveAPIView):
    """
    Handles GET requests to retrieve a single Book by its primary key (pk).
    - Accessible to everyone (no authentication required).
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]


# -----------------------------
# CREATE VIEW
# -----------------------------
class BookCreateView(generics.CreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        """
        Optionally attach the request user to the book creation.
        This is just an example — since Book has an author ForeignKey,
        you could set author=self.request.user if using a custom user model.
        """
        serializer.save()



# -----------------------------
# UPDATE VIEW
# -----------------------------
class BookUpdateView(generics.UpdateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]

    def perform_update(self, serializer):
        """
        Customize update behavior — for example, log updates or enforce rules.
        """
        serializer.save()

# -----------------------------
# DELETE VIEW
# -----------------------------
class BookDeleteView(generics.DestroyAPIView):
    """
    Handles DELETE requests to remove an existing Book.
    - Restricted to authenticated users.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]



class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission: allow read to anyone, write only to owner.
    Assumes the Book model has an 'author' field linked to User.
    """

    def has_object_permission(self, request, view, obj):
        # SAFE_METHODS are GET, HEAD, OPTIONS
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user
