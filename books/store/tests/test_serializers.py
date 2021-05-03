from django.contrib.auth.models import User
from django.db.models import Count, Case, When
from django.test import TestCase

from store.models import Book, UserBookRelation
from store.serializer import BooksSerializer


class BookSerializerTestCase(TestCase):
    def test_ok(self):
        user1 = User.objects.create(username='user1')
        user2 = User.objects.create(username='user2')
        user3 = User.objects.create(username='user3')
        book_one = Book.objects.create(name='first_book', price=300,
                                       author_name='Author 1')
        book_two = Book.objects.create(name='second_book', price=200,
                                       author_name='Author 2')

        UserBookRelation.objects.create(user=user1, book=book_one, like=True)
        UserBookRelation.objects.create(user=user2, book=book_one, like=True)
        UserBookRelation.objects.create(user=user3, book=book_one, like=True)

        books = Book.objects.all().annotate(
            annotated_likes=Count(Case(When(userbookrelation__like=True, then=1)))).order_by('id')
        data = BooksSerializer(books, many=True).data
        expected_data = [
            {
                'id': book_one.id,
                'name': 'first_book',
                'price': '300.00',
                'author_name': 'Author 1',
                'likes_count': 3,
                'annotated_likes': 3
            },
            {
                'id': book_two.id,
                'name': 'second_book',
                'price': '200.00',
                'author_name': 'Author 2',
                'likes_count': 0,
                'annotated_likes': 0
            },
        ]
        print(expected_data)
        print(data)
        self.assertEqual(expected_data, data)
