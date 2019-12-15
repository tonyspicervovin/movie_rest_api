from django.test import TestCase
from django.test import TestCase
from django.db import models

from django.contrib.auth.models import User
from django.db import IntegrityError

class TestUser(TestCase):

    def test_add_movie(self):
        movie = Movie(user = 'tony', name = 'scarface', overview = 'crime movie', genres = 'drama', date = '10-25-93')
        movie.save()

        movies = Movie.objects.get(name = "scarface")
        self.assertEqual(len(movies), 1)
    #testing adding to the db
    def test_add_movie_wrong_fields(self):
        movie = Movie(user = 'tony', name = 'scarface', overview = 'crime movie', genres = 'drama', date = '10-25-93')
        movie.save()
        movie2 = Movie(user = 'tony', named = 'scarface', overview = 'crime movie', genres = 'drama', date = '10-25-93')
        with self.assertRaises(IntegrityError):
            movie2.save()
    # testing adding a movie with the wrong fields
    def test_add_duplicate_movie(self):
        movie = Movie(user = 'tony', name = 'scarface', overview = 'crime movie', genres = 'drama', date = '10-25-93')
        movie.save()
        movie2 = Movie(user = 'tony', name = 'scarface', overview = 'crime movie', genres = 'drama', date = '10-25-93')
        with self.assertRaises(IntegrityError):
            movie2.save()
    #testing adding a duplicate movie
    def test_add_duplicate_user(self):
        user = User(username="tony", email='ton@ton.com', first_name='tony', last_name='bob')
        user.save()
        user2 = User(username="tony", email='ton@ton.com', first_name='tony', last_name='bob')
        with self.assertRaises(IntegrityError):
            user2.save()
    #testing adding a duplicate user

# Create your tests here.
