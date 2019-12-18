from django.shortcuts import render
from rest_framework import viewsets 
from movieapi.restapi.serializers import MovieSerializer
from movieapi.restapi.models import Movie
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.db.utils import IntegrityError
from django.http import HttpResponse


def homepage(request):
    return HttpResponse('Hello World')


class MovieViewSet(viewsets.ModelViewSet):
    # queryset = Movie.objects.filter(user=request.user).order_by('name')
    # queryset = Movie.objects.all().order_by('name')

    serializer_class = MovieSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # return self.request.user.movies.all()
        return Movie.objects.filter(user=self.request.user).order_by('name')

    def create(self, request):
        try:
            print("creating", request.data)
            movie = Movie(name=request.data['name'], overview=request.data['overview'], genres=request.data['genres'], date=request.data['date'], rating=request.data['rating'],user=request.user).save()
            return Response(movie, status=status.HTTP_201_CREATED)
        except IntegrityError as e:
            print(e)
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)
