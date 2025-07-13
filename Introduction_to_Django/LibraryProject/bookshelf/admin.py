from django.contrib import admin

from .models import Book

class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'publication_year')  # Show these fields in the list view
    list_filter = ('author', 'publication_year')           # Add filters for author and year
    search_fields = ('title', 'author')                    # Enable search by title and author

admin.site.register(Book, BookAdmin)
