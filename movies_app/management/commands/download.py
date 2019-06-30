from os import mkdir

import requests
import re

from django.conf import settings
from django.core.files import File
from django.core.files.storage import FileSystemStorage

from django.core.management.base import BaseCommand

from movies_app.models import *


class Command(BaseCommand):
    """Class must inherit from BaseCommand"""

    help = 'fetch movies from OMDB API'

    def add_arguments(self, parser):
        """
        method to give parameters to the handle method
        Args:
            parser: (str) to allow pass movie title and -s parameter to the search

        Returns: None

        """

        parser.add_argument('title', type=str)
        """positional argument"""


        parser.add_argument('-s', '--search', action='store_true', default=False)
        """kwargs like arguments"""

    def handle(self, *args, **options):
        """
        method to invoke main method when command is executed
        Args:
            *args: not used here
            **options: catch the parameters passing through the add_arguments method

        Returns: (str) downloaded movie's title

        """

        search = options['search']
        title = options['title']

        if search:
            url = 'http://www.omdbapi.com/?s='+title+'&apikey=8679f1c&type=movie'
            list=requests.get(url)
            for i in list.json()['Search']:
                code = i['imdbID']
                l_url = 'http://www.omdbapi.com/?i='+code+'&apikey=8679f1c&type=movie'
                Command.save_movie(l_url)
        else:
            url = 'http://www.omdbapi.com/?t='+title+'&apikey=8679f1c&type=movie'
            if Command.save_movie(url):
                return str(title)
            else:
                return 'It was no possible download a movie with parameter: ' + str(title)


    @staticmethod
    def save_image(poster_url,title):
        """
        method to storage an image
        Args:
            poster_url: url where poster is finded
            title: movie's title

        Returns: (str) path where the image was storaged

        """
        relative = '/movie/'+title+'/'
        fs = FileSystemStorage(location='media/'+relative)
        if poster_url != "N/A":
            ext = poster_url[-3:]
            mkdir(settings.MEDIA_ROOT+relative)
            up_file = requests.get(poster_url)
            my_file = File(open(settings.MEDIA_ROOT+relative+'myImage.' + ext, 'wb'))
            my_file.name = 'myImage.' + ext
            my_file.write(up_file.content)
        else:
            my_file = File(open('media/myImage.jpg','rb'))
            my_file.name = 'myImage.jpg'
            fs.save(my_file.name,my_file)

        my_file.close()
        return relative+my_file.name

    @staticmethod
    def save_movie(url):
        """
        static method for allow be called anywhere, it storage a movie, a director and an actor to the database
        Args:
            url: resource url, it depends to the search option

        Returns: (bool) return True if the movie can be donwloaded

        """
        peli = requests.get(url)
        g = Genre.objects.get_or_create(name=peli.json()['Genre'].split(", ")[0], defaults={'description': 'whatever'})
        l = Language.objects.get_or_create(name=peli.json()['Language'].split(", ")[0])
        c = Country.objects.get_or_create(name=peli.json()['Country'].split(", ")[0])
        m = Movie.objects.get_or_create(title=peli.json()['Title'], defaults={
            'duration': int((peli.json()['Runtime']).split()[0]),
            'poster': Command.save_image(peli.json()['Poster'], re.sub('[^a-zA-Z0-9]', '', peli.json()['Title'])),
            'detail': peli.json()['Plot'],
            'genre': g[0],
            'original_language': l[0],
            'country': c[0],
        })
        d=Director.objects.get_or_create(name = peli.json()['Director'].split(", ")[0], defaults={
            'age':0,
        })
        a=Actor.objects.get_or_create(name=peli.json()['Actors'].split(", ")[0], defaults={
            'age': 0,
        })
        d[0].movie.add(m[0])
        a[0].movie.add(m[0])

        return m[1]

