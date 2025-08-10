from rest_framework import serializers
from datetime import datetime
from .models import Author, Book

class BookSerializer(serializers.ModelSerializer):

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

    class Meta:
        model = Book
        fields = ['id', 'title', 'publication_year']


class AuthorSerializer(serializers.ModelSerializer):
    books = BookSerializer(many=True, read_only=True)

    class Meta:
        model = Author
        fields = ['id', 'name', 'books']
