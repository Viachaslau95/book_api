from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from store.serializer import BooksSerializer

from store.models import Book


class BooksApiTestCase(APITestCase):
    def setUp(self):
        self.book_one = Book.objects.create(name='first_book', price=300,
                                            author_name='Author 1')
        self.book_two = Book.objects.create(name='second_book', price=200,
                                            author_name='Author 2')
        self.book_three = Book.objects.create(name='three_book Author 1', price=200,
                                              author_name='Author 3')

    def test_get(self):
        url = reverse('book-list')
        response = self.client.get(url)
        serializer_data = BooksSerializer([self.book_one, self.book_two, self.book_three], many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)

    def test_get_filter(self):
        url = reverse('book-list')
        response = self.client.get(url, data={'price': 200})
        serializer_data = BooksSerializer([self.book_two,
                                           self.book_three], many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)

    def test_get_search(self):
        url = reverse('book-list')
        response = self.client.get(url, data={'search': 'Author 1'})
        serializer_data = BooksSerializer([self.book_one, self.book_three], many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)
