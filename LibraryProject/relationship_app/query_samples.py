from relationship_app.models import Author, Book, Library, Librarian

# Query all books by a specific author
author_name = "J.K. Rowling"
try:
    author = Author.objects.get(name=author_name)
    books_by_author = author.books.all()
    print(f"Books by {author.name}:")
    for book in books_by_author:
        print(f"- {book.title}")
except Author.DoesNotExist:
    print(f"No author found with name '{author_name}'.")

# List all books in a library
library_name = "Central Library"
try:
    library = Library.objects.get(name=library_name)
    books_in_library = library.books.all()
    print(f"\nBooks in {library.name}:")
    for book in books_in_library:
        print(f"- {book.title}")
except Library.DoesNotExist:
    print(f"No library found with name '{library_name}'.")

# Retrieve the librarian for a library
try:
    librarian = library.librarian  # uses related_name='librarian'
    print(f"\nLibrarian of {library.name}: {librarian.name}")
except Librarian.DoesNotExist:
    print(f"No librarian assigned to {library.name}")

# Get a specific author (example: "J.K. Rowling")
    author_name = "J.K. Rowling"
try:
    author = Author.objects.get(name=author_name)

    
    books_by_author = Book.objects.filter(author=author)

    print(f"Books by {author.name}:")
    for book in books_by_author:
        print(f"- {book.title}")

except Author.DoesNotExist:
    print(f"No author found with name '{author_name}'.")

library_name = "Central Library"

try:
    library = Library.objects.get(name=library_name)

    
    librarian = Librarian.objects.get(library=library)

    print(f"Librarian for {library.name}: {librarian.name}")

except Library.DoesNotExist:
    print(f"No library found with name '{library_name}'.")

except Librarian.DoesNotExist:
    print(f"No librarian assigned to {library.name}.")