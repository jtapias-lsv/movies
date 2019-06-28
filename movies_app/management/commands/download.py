from os import mkdir

import requests
import re

from django.conf import settings
from django.core.files import File
from django.core.files.storage import FileSystemStorage

from django.core.management.base import BaseCommand

from movies_app.models import *


class Command(BaseCommand):
    help = 'fetch movies from OMDB API'

    def add_arguments(self, parser):
        # positional argument
        parser.add_argument('title', type=str)

        # kwargs like arguments
        parser.add_argument('-s', '--search', action='store_true', default=False)


    def handle(self, *args, **options):
        search = options['search']
        title = options['title']

        if search:
            url = 'http://www.omdbapi.com/?s='+title+'&apikey=8679f1c&type=movie'
            lista=requests.get(url)
            for i in lista.json()['Search']:
                codigo = i['imdbID']
                l_url = 'http://www.omdbapi.com/?i='+codigo+'&apikey=8679f1c&type=movie'
                Command.saveMovie(l_url)
        else:
            url = 'http://www.omdbapi.com/?t='+title+'&apikey=8679f1c&type=movie'
            if Command.saveMovie(url):
                return str(title)
            else:
                return 'No se pudo descargar una pelicula con el parametro: ' + str(title)


    @staticmethod
    def saveImage(poster_url,title):
        relativo = '/movie/'+title+'/'
        fs = FileSystemStorage(location='media/'+relativo)
        if poster_url != "N/A":
            ext = poster_url[-3:]
            mkdir(settings.MEDIA_ROOT+relativo)
            up_file = requests.get(poster_url)
            my_file = File(open(settings.MEDIA_ROOT+relativo+'myImage.' + ext, 'wb'))
            my_file.name = 'myImage.' + ext
            my_file.write(up_file.content)
        else:
            my_file = File(open('media/myImage.jpg','rb'))
            my_file.name = 'myImage.jpg'
            fs.save(my_file.name,my_file)

        my_file.close()
        return relativo+my_file.name

    @staticmethod
    def saveMovie(url):
        peli = requests.get(url)
        g = Genre.objects.get_or_create(name=peli.json()['Genre'].split(", ")[0], defaults={'description': 'whatever'})
        l = Language.objects.get_or_create(name=peli.json()['Language'].split(", ")[0])
        c = Country.objects.get_or_create(name=peli.json()['Country'].split(", ")[0])
        m = Movie.objects.get_or_create(title=peli.json()['Title'], defaults={
            'duration': int((peli.json()['Runtime']).split()[0]),
            'poster': Command.saveImage(peli.json()['Poster'], re.sub('[^a-zA-Z0-9]', '', peli.json()['Title'])),
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

