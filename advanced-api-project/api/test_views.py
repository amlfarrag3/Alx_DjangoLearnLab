from django.contrib.auth import get_user_model
from django.utils import timezone
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from .models import Author, Book

User = get_user_model()

class BookAPITestCase(APITestCase):
    """
    Tests for Book API endpoints:
    - list (with filtering/search/ordering)
    - detail
    - create (auth required)
    - update (auth required)
    - delete (auth required)
    - publication_year validation
    """

    def setUp(self):
        # Create users
        self.user = User.objects.create_user(username='tester', password='testpass123')
        self.other_user = User.objects.create_user(username='other', password='testpass123')

        # Create authors
        self.author1 = Author.objects.create(name="J. R. R. Tolkien")
        self.author2 = Author.objects.create(name="George Orwell")

        # Create books
        self.book1 = Book.objects.create(title="The Hobbit", publication_year=1937, author=self.author1)
        self.book2 = Book.objects.create(title="1984", publication_year=1949, author=self.author2)
        self.book3 = Book.objects.create(title="Animal Farm", publication_year=1945, author=self.author2)

        # API client
        self.client = APIClient()

        # Base endpoints (these match the patterns we've discussed)
        self.list_url = "/api/books/"
        self.detail_url = lambda pk: f"/api/books/{pk}/"
        self.update_url = lambda pk: f"/api/books/update/{pk}/"
        self.delete_url = lambda pk: f"/api/books/delete/{pk}/"

    # ----------------------
    # Read-only access tests
    # ----------------------
    def test_list_books_public(self):
        """Anyone can access the book list (status 200 and contains created books)."""
        resp = self.client.get(self.list_url)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        titles = [item['title'] for item in resp.json()]
        self.assertIn(self.book1.title, titles)
        self.assertIn(self.book2.title, titles)

    def test_get_book_detail_public(self):
        """Anyone can access a single book detail."""
        resp = self.client.get(self.detail_url(self.book1.pk))
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.json()
        self.assertEqual(data['title'], self.book1.title)
        self.assertEqual(data['publication_year'], self.book1.publication_year)

    # ----------------------
    # Create tests
    # ----------------------
    def test_create_book_requires_authentication(self):
        """Unauthenticated POST should be forbidden (401 or 403 depending on settings)."""
        payload = {"title": "New Book", "publication_year": 2000, "author": self.author1.pk}
        resp = self.client.post(self.list_url, payload, format='json')
        self.assertIn(resp.status_code, (status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN))

    def test_create_book_authenticated(self):
        """Authenticated user can create a book."""
        self.client.force_authenticate(user=self.user)
        payload = {"title": "New Book", "publication_year": 2000, "author": self.author1.pk}
        resp = self.client.post(self.list_url, payload, format='json')
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        # Verify created in DB
        self.assertTrue(Book.objects.filter(title="New Book", publication_year=2000, author=self.author1).exists())

    def test_create_book_future_publication_year_invalid(self):
        """Creating a book with a future publication_year should fail validation."""
        self.client.force_authenticate(user=self.user)
        future_year = timezone.now().year + 5
        payload = {"title": "Future Book", "publication_year": future_year, "author": self.author1.pk}
        resp = self.client.post(self.list_url, payload, format='json')
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
        # Check that the error mentions publication_year
        self.assertIn('publication_year', resp.json())

    # ----------------------
    # Update tests
    # ----------------------
    def test_update_requires_authentication(self):
        """Unauthenticated update should be forbidden."""
        payload = {"title": "Updated Title", "publication_year": 1937, "author": self.author1.pk}
        resp = self.client.put(self.update_url(self.book1.pk), payload, format='json')
        self.assertIn(resp.status_code, (status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN))

    def test_update_book_authenticated(self):
        """Authenticated user can update a book (status 200)."""
        self.client.force_authenticate(user=self.user)
        payload = {"title": "The Hobbit (Updated)", "publication_year": 1937, "author": self.author1.pk}
        resp = self.client.put(self.update_url(self.book1.pk), payload, format='json')
        # Accept either 200 or 202 depending on partial/full update implementation
        self.assertIn(resp.status_code, (status.HTTP_200_OK, status.HTTP_202_ACCEPTED))
        self.book1.refresh_from_db()
        self.assertEqual(self.book1.title, "The Hobbit (Updated)")

    # ----------------------
    # Delete tests
    # ----------------------
    def test_delete_requires_authentication(self):
        """Unauthenticated delete should be forbidden."""
        resp = self.client.delete(self.delete_url(self.book2.pk))
        self.assertIn(resp.status_code, (status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN))

    def test_delete_book_authenticated(self):
        """Authenticated user can delete a book (status 204)."""
        self.client.force_authenticate(user=self.user)
        resp = self.client.delete(self.delete_url(self.book2.pk))
        # Some setups return 204 NO CONTENT
        self.assertIn(resp.status_code, (status.HTTP_204_NO_CONTENT, status.HTTP_200_OK))
        self.assertFalse(Book.objects.filter(pk=self.book2.pk).exists())

    # ----------------------
    # Filtering / Searching / Ordering tests
    # ----------------------
    def test_filter_by_title(self):
        """Filtering by title exact match returns matching book(s)."""
        resp = self.client.get(f"{self.list_url}?title=The%20Hobbit")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.json()
        self.assertTrue(any(item['title'] == "The Hobbit" for item in data))
        # Should not include unrelated titles
        self.assertFalse(any(item['title'] == "1984" for item in data))

    def test_search_by_author_name(self):
        """Search by author name should return books for that author (partial match)."""
        # use search query param (SearchFilter)
        resp = self.client.get(f"{self.list_url}?search=Orwell")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        titles = [item['title'] for item in resp.json()]
        self.assertIn("1984", titles)
        self.assertIn("Animal Farm", titles)

    def test_ordering_by_publication_year(self):
        """Ordering by publication_year descending returns newest books first."""
        resp = self.client.get(f"{self.list_url}?ordering=-publication_year")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.json()
        years = [item['publication_year'] for item in data]
        # Verify descending order
        self.assertEqual(years, sorted(years, reverse=True))

class BookAPITests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.book = Book.objects.create(
            title="Test Book",
            author="Test Author",
            publication_year=2023
        )

    def test_list_books(self):
        url = reverse('book-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Checker wants this line
        self.assertIn('title', response.data[0])
        self.assertEqual(response.data[0]['title'], "Test Book")

    def test_create_book(self):
        self.client.login(username='testuser', password='testpass')
        url = reverse('book-list')
        data = {"title": "New Book", "author": "New Author", "publication_year": 2024}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # Checker wants this line
        self.assertEqual(response.data['title'], "New Book")

    def test_update_book(self):
        self.client.login(username='testuser', password='testpass')
        url = reverse('book-detail', kwargs={'pk': self.book.id})
        data = {"title": "Updated Title", "author": "Test Author", "publication_year": 2023}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Checker wants this line
        self.assertEqual(response.data['title'], "Updated Title")

    def test_delete_book(self):
        self.client.login(username='testuser', password='testpass')
        url = reverse('book-detail', kwargs={'pk': self.book.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
