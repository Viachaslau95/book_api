from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.utils import json

from store.serializer import BooksSerializer

from store.models import Book, UserBookRelation


class BooksApiTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(username='test_username')
        self.book_one = Book.objects.create(name='first_book', price=300,
                                            author_name='Author 1', owner=self.user)
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

    def test_create(self):
        self.assertEqual(3, Book.objects.all().count())
        url = reverse('book-list')
        data = {
            'name': 'test_book',
            'price': 123,
            'author_name': 'test_author'
        }
        json_data = json.dumps(data)
        self.client.force_login(self.user)
        response = self.client.post(url, data=json_data,
                                    content_type='application/json')
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(4, Book.objects.all().count())
        self.assertEqual(self.user, Book.objects.last().owner)

    def test_update(self):
        url = reverse('book-detail', args=(self.book_one.id,))
        data = {
            'name': self.book_one.name,
            'price': 3548,
            'author_name': self.book_one.author_name
        }
        json_data = json.dumps(data)
        self.client.force_login(self.user)
        response = self.client.put(url, data=json_data,
                                   content_type='application/json')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        # self.book_one = Book.objects.get(id=self.book_one.id)
        self.book_one.refresh_from_db()
        self.assertEqual(3548, self.book_one.price)


class BooksRelationTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(username='test_username')
        self.user2 = User.objects.create(username='test_username2')
        self.book_one = Book.objects.create(name='first_book', price=300,
                                            author_name='Author 1', owner=self.user)
        self.book_two = Book.objects.create(name='second_book', price=200,
                                            author_name='Author 2')

    def test_like(self):
        url = reverse('userbookrelation-detail', args=(self.book_one.id,))

        data = {
            'like': True
        }
        json_data = json.dumps(data)
        self.client.force_login(self.user)

        response = self.client.patch(url, data=json_data,
                                     content_type='application/json')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        relation = UserBookRelation.objects.get(user=self.user,
                                                book=self.book_one)
        self.assertTrue(relation.like)


