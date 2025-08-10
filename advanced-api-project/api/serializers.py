# api/serializers.py
from rest_framework import serializers
from datetime import datetime
from .models import Author, Book

class BookSerializer(serializers.ModelSerializer):
    """
    Serializes Book model fields.
    Custom validation ensures publication_year is not in the future.
    """
    class Meta:
        model = Book
        fields = ['id', 'title', 'publication_year', 'author']
        read_only_fields = ['id']

    def validate_publication_year(self, value):
        """
        Validate that the publication year is not in the future.
        Raise a serializers.ValidationError if it is.
        """
        current_year = datetime.now().year
        if value > current_year:
            raise serializers.ValidationError(f"publication_year ({value}) cannot be in the future (current year {current_year}).")
        return value


class BookNestedSerializer(serializers.ModelSerializer):
    """
    A lightweight nested serializer for Book to use inside AuthorSerializer.
    We omit the 'author' field here to avoid circular nesting.
    """
    class Meta:
        model = Book
        fields = ['id', 'title', 'publication_year']


class AuthorSerializer(serializers.ModelSerializer):
    """
    Serializes an Author and their related books:
    - name: main author field
    - books: a nested list of BookNestedSerializer instances representing all
      books related to this author (using the `related_name='books'` from the model).
    """
    # Use source='books' because Author model related_name is 'books'
    books = BookNestedSerializer(source='books', many=True, read_only=True)

    class Meta:
        model = Author
        fields = ['id', 'name', 'books']
        read_only_fields = ['id', 'books']
