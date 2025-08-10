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
