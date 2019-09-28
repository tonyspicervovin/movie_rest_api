from django.shortcuts import render
from rest_framework import viewsets 
from movieapi.restapi.serializers import MovieSerializer
from movieapi.restapi.models import Movie


class MovieViewSet(viewsets.ModelViewSet):
    # queryset = Movie.objects.filter(user=request.user).order_by('name')
    queryset = Movie.objects.filter().order_by('name')

    serializer_class = MovieSerializer