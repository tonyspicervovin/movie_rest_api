from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.

class Movie(models.Model):
    user = models.ForeignKey('auth.User', blank=False, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, blank=False, null=False)
    overview = models.CharField(max_length=1000, blank=False, null=False)
    genres = models.CharField(max_length=500, blank=False, null=False)
    date = models.CharField(max_length=200, blank=False, null=False)
    rating = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(5)])
    
    class Meta:
        unique_together = [ ['user', 'name' ] ]

    def __str__(self):
        return f'Movie {self.id}. Name: {self.name} overview: {self.overview} genres: {self.overview} date: {self.date} rating: {self.rating} belongs to {self.user}'