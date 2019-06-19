from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
import uuid

from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.urls import reverse_lazy

from .choices import THRILLER, MOVIE_GENRE
from .queryset import *


from django.contrib.auth.models import AbstractUser
from django.utils.text import slugify



# para hacer referencia al usuario del sistema
User = get_user_model()

# para definir donde se almacenarán los posters
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
    title = models.CharField(max_length=100)
    duration = models.PositiveIntegerField()
    poster = models.ImageField(upload_to=movie_directory_path)
    about = models.CharField(max_length=300, default='a movie')
    detail = models.TextField(null=True, blank=True)
    trailer_url = models.URLField(null=True, blank=True)
    genre = models.ForeignKey(Genre,on_delete=models.CASCADE)
    #genre = models.CharField(max_length=25, choices=MOVIE_GENRE, default=THRILLER)
    original_language = models.ForeignKey(Language,on_delete = models.CASCADE)
    release_date = models.DateField(null=True)
    country = models.ForeignKey(Country,on_delete=models.CASCADE)
    slug = models.CharField(max_length=100, null=True, blank=True)

    #own_objects = MovieQuerySet.as_manager()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse_lazy('movies_app:movie_detail',args=(self.title,))

    # def save(self, force_insert=False, force_update=False, using=None,
    #          update_fields=None):
    #     self.slug = slugify(self.title)
    #     super(Movie,self).save(force_insert=force_insert,force_update=force_update, using=using,
    #                            update_fields=update_fields)


class Director(models.Model):
    """Contain all director that manage movies"""
    name = models.CharField(max_length=50)
    age = models.PositiveIntegerField()
    movie = models.ManyToManyField(Movie)
    alive = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Actor(models.Model):
    """Contain all actors that acts in movies"""
    name = models.CharField(max_length=50)
    age = models.PositiveIntegerField()
    movie = models.ManyToManyField(Movie)
    alive = models.BooleanField(default=True)
    
    def __str__(self):
        return self.name

class Rate(models.Model):
    """Contins all comments that users made"""
    rate = models.FloatField(validators=[MinValueValidator(0),MaxValueValidator(5)])
    movie = models.ForeignKey(Movie,on_delete = models.CASCADE)
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    comment = models.CharField(max_length=200, null=True)

    objects = MovieRateQuerySet.as_manager()

    class Meta:
        unique_together = ('user', 'movie')
        permissions = (
            ('can_vote_two_times','Can vote two times'),
        )

    def __str__(self):
        return f'{self.user.username} : {self.movie.title}'



class ValidatorToken(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    unique_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)