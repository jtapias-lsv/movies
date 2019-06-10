from django.contrib.auth import get_user_model
from django.db import models
from django.contrib.auth.models import AbstractUser

User = get_user_model()

def movie_directory_path(instance,filename):
    return f'movie/{instance.title}/{filename}'

class Genre(models.Model):
    """Contains all gender of movies"""
    name = models.CharField(max_length=20)
    description = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Language(models.Model):
    """Contains all posible language """
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Country(models.Model):
    """Contain all contry where movies are meked"""
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name



class Movie(models.Model):
    """Constins all information of a movie"""
    title = models.CharField(max_length=50)
    duration = models.PositiveIntegerField()
    poster = models.ImageField(upload_to=movie_directory_path)
    detail = models.CharField(max_length=100)
    trailer_url = models.URLField()
    genre = models.ForeignKey(Genre,on_delete=models.CASCADE)
    original_language = models.ForeignKey(Language,on_delete = models.CASCADE)
    release_date = models.DateField()
    country = models.ForeignKey(Country,on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Director(models.Model):
    """Contain all director that manage movies"""
    name = models.CharField(max_length=50)
    age = models.IntegerField()
    movie = models.ManyToManyField(Movie)

    def __str__(self):
        return self.name


class Actor(models.Model):
    """Contain all actors that acts in movies"""
    name = models.CharField(max_length=50)
    age = models.IntegerField()
    movie = models.ManyToManyField(Movie)
    
    def __str__(self):
        return self.name

class Rate(models.Model):
    """Contins all comments that users made"""
    rate = models.PositiveIntegerField()
    movie = models.ForeignKey(Movie,on_delete = models.CASCADE)
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    comment = models.CharField(max_length=200)

    def __str__(self):
        return self.user.username +" - "+self.movie.title