from django.test import TestCase
from django.test import TestCase
from django.db import models
from .models import Movie
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.test import APIRequestFactory

from rest_framework.test import APIRequestFactory, force_authenticate, APIClient 
from rest_framework.authtoken.models import Token


class TestUser(TestCase):

    def test_add_movie(self):
        user = User(username='bob', email='bob@bob.com', first_name='bob', last_name='bob')
        user.save()        
        movie = Movie(user = user, name = 'scarface', overview = 'crime movie', genres = 'drama', date = '10-25-93', rating = 2.5)
        movie.save()
        response = Movie.objects.get(name = 'scarface')
        expected_overview = 'crime movie'
        self.assertEqual(response.overview, expected_overview)
    #testing adding to the db
    def test_add_movie_wrong_fields(self):
        user = User(username='bob', email='bob@bob.com', first_name='bob', last_name='bob')
        user.save()         
        movie = Movie(user = user, name = 'scarface', overview = 'crime movie', genres = 'drama', date = '10-25-93', rating = 5.0)
        movie.save()
        with self.assertRaises(TypeError):
            movie2 = Movie(user = user, nameie = 'scarface', overview = 'crime movie', genres = 'drama', date = '10-25-93', rating = 5.0)
            movie2.save()
    # testing adding a movie with the wrong fields
    def test_add_duplicate_movie(self):
        user = User(username='bob', email='bob@bob.com', first_name='bob', last_name='bob')
        user.save() 
        movie = Movie(user = user, name = 'scarface', overview = 'crime movie', genres = 'drama', date = '10-25-93', rating = 4.5)
        movie.save()
        movie2 = Movie(user = user, name = 'scarface', overview = 'crime movie', genres = 'drama', date = '10-25-93', rating = 5.0)
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
    def test_delete_object(self):
        user = User(username="tony", email='ton@ton.com', first_name='tony', last_name='bob')
        user.save()
        movie = Movie(user = user, name = 'scarface', overview = 'crime movie', genres = 'drama', date = '10-25-93', rating = 4.5)
        movie.save()
        response = Movie.objects.get(name = 'scarface')
        movie.delete()
        with self.assertRaises(ObjectDoesNotExist):
            response = Movie.objects.get(name = 'scarface')
    #testing that we can add a user, make a query and than delete the user and the query returns does not exist 
    
    def test_update_obect(self):
        user = User(username="tony", email='ton@ton.com', first_name='tony', last_name='bob')
        user.save()
        movie = Movie(user = user, name = 'scarface', overview = 'crime movie', genres = 'drama', date = '10-25-93', rating = 4.5)
        movie.save()
        movie.rating = 3.0
        movie.save()
        self.assertEqual(movie.rating, 3.0)


class TestRoute(TestCase):

    #  TODO fixtures may be helpful to insert test data into database 
    #  See LMN for example 

    def setUp(self):

        # probably need these for many test methods
        self.tony = User()
        self.tony.save()
        self.token = Token.objects.create(user=self.tony)

        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)    


    def test_post_movies(self):

        # https://www.django-rest-framework.org/api-guide/testing/
        
        movie_data = {'user': self.tony.id, 'name': 'example', 'overview': 'is is a movie', 'genres': 'drama', 'date': '01-01-2001', 'rating': 3}
        response = self.client.post('/api/movies/', movie_data, follow=True)
        self.assertEqual(201, response.status_code)

    def test_post_too_high_rating(self):
        movie_data = {'user': self.tony.id, 'name': 'example', 'overview': 'is is a movie', 'genres': 'drama', 'date': '01-01-2001', 'rating': 10}
        response = self.client.post('/api/movies/', movie_data, follow=True)
        self.assertEqual(400, response.status_code)

    def test_get_movies(self):
        movie_data = {'user': self.tony.id, 'name': 'example', 'overview': 'is is a movie', 'genres': 'drama', 'date': '01-01-2001', 'rating': 3}
        response = self.client.post('/api/movies/', movie_data, follow=True)
        response2 = self.client.get('/api/movies/', movie_data, follow=True)
        print(response2.json())
        self.assertEqual(200, response2.status_code)

    def test_patch_movies(self):

        movie_data = {'user': self.tony.id, 'name': 'example', 'overview': 'is is a movie', 'genres': 'drama', 'date': '01-01-2001', 'rating': 3}
        response = self.client.post('/api/movies/', movie_data, follow=True)
        movie_data = {'user': self.tony.id, 'name': 'example', 'overview': 'is is a movie', 'genres': 'drama', 'date': '01-01-2001', 'rating': 4}
        response2 = self.client.patch('/api/movies/1', movie_data, follow=True)
        movie = self.client.get('/api/movies/1')
        print("name  " + movie.name)
        self.assertEqual(200, response2.status_code)

    def test_delete_movie(self):
        user = User(username='bob', email='bob@bob.com', first_name='bob', last_name='bob')
        user.save()
        movie = Movie(user = user, name = 'scarface', overview = 'crime movie', genres = 'drama', date = '10-25-93', rating = 2.5)
        movie.save()
        route = f'/api/movies/{movie.id}/'
        response2 = self.client.delete(route, follow=True)
        self.assertEqual(200, response2.status_code)

    def test_get_one_movie(self):
        user = User(username='bob', email='bob@bob.com', first_name='bob', last_name='bob')
        user.save()
        movie = Movie(user = user, name = 'scarface', overview = 'crime movie', genres = 'drama', date = '10-25-93', rating = 2.5)
        movie.save()
        route = f'/api/movies/{movie.id}/'
        response = self.client.get(route, follow=True)
        self.assertEqual(200, response.status_code)

# Create your tests here.
