from django.contrib import admin

from .models import Genre, Language,Country, Actor, Director, Movie, Rate, Suggestion

# Register your models here.
admin.site.register(Genre)
admin.site.register(Language)
admin.site.register(Country)
admin.site.register(Actor)
admin.site.register(Director)
admin.site.register(Movie)
admin.site.register(Rate)
admin.site.register(Suggestion)