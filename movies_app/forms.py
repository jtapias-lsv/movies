from django import forms

from .models import *


class GenreCreateForm(forms.ModelForm):

    class Meta:
        model = Genre
        fields = ('name','description')


class MoviesCreateView(forms.ModelForm):

    class Meta:
        model = Movie
        fields = '__all__'