from django.contrib import admin

from .models import *

# Register your models here.
admin.site.register(Genre)
admin.site.register(Language)
admin.site.register(Country)
admin.site.register(Actor)
admin.site.register(Director)
admin.site.register(Movie)
admin.site.register(Rate)