from django.shortcuts import render
from rest_framework import viewsets 
from movieapi.restapi.serializers import MovieSerializer
from movieapi.restapi.models import Movie
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.db.utils import IntegrityError


class MovieViewSet(viewsets.ModelViewSet):
    # queryset = Movie.objects.filter(user=request.user).order_by('name')
    # queryset = Movie.objects.all().order_by('name')

    serializer_class = MovieSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # return self.request.user.movies.all()
        print(self.request.user)
        return Movie.objects.filter(user=self.request.user).order_by('name')

    def create(self, request):
        try:
            movie = Movie(name=request.data['name'], rating=request.data['rating'], user=request.user).save()
            return Response('ok', status=status.HTTP_201_CREATED)
        except IntegrityError as e:
            print(e)
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)
