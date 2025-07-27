from django.contrib.auth.decorators import permission_required
from django.shortcuts import render, get_object_or_404
from .models import Book
from .forms import ExampleForm


@permission_required('bookshelf.can_view', raise_exception=True)
def book_list(request):
    books = Book.objects.all()
    return render(request, 'bookshelf/book_list.html', {'books': books})

@permission_required('bookshelf.can_edit', raise_exception=True)
def edit_book(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    # Handle form/edit logic here
    return render(request, 'bookshelf/edit_book.html', {'book': book})


def search_books(request):
    query = request.GET.get('q', '')
    books = Book.objects.filter(title__icontains=query)
    return render(request, 'bookshelf/book_list.html', {'books': books})

def example_form_view(request):
    form = ExampleForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        # process form.cleaned_data here
        return render(request, 'bookshelf/form_success.html')
    return render(request, 'bookshelf/form_example.html', {'form': form})
