from django.test import TestCase

from store.models import Book
from store.serializer import BooksSerializer


class BookSerializerTestCase(TestCase):
    def test_ok(self):
        book_one = Book.objects.create(name='first_book', price=300)
        book_two = Book.objects.create(name='second_book', price=200)
        data = BooksSerializer([book_one, book_two], many=True).data
        expected_data = [
            {
                'id': book_one.id,
                'name': 'first_book',
                'price': '300.00'
            },
            {
                'id': book_two.id,
                'name': 'second_book',
                'price': '200.00'
            },
        ]
        self.assertEqual(expected_data, data)
