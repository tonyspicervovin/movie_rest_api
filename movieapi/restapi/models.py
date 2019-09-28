from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.

class Movie(models.Model):
    user = models.ForeignKey('auth.User', blank=False, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, blank=False, null=False, unique=True)
    rating = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(5)])

    def __str__(self):
        return f'Movie {self.id}. Name: {self.name} rating: {self.rating}'