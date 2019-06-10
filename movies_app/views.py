from django.views.generic import ListView, CreateView, UpdateView
from django.urls import reverse_lazy

from .models import Genre
from .forms import *

class GenreListView(ListView):
    model = Genre
    template_name = 'lista_genre.html'


class GenreCreateView(CreateView):
    model = Genre
    form_class = GenreCreateForm
    template_name = 'info_genre.html'
    success_url = reverse_lazy('movies_app:list_genre')


class GenreUpdateView(UpdateView):
    model = Genre
    form_class = GenreCreateForm
    template_name = 'info_genre.html'
    success_url = reverse_lazy('movies_app:list_genre')


class MovieListView(ListView):
    model = Genre
    template_name = 'lista_genre.html'


class MovieCreateView(CreateView):
    model = Genre
    form_class = GenreCreateForm
    template_name = 'info_genre.html'
    success_url = reverse_lazy('movies_app:list_genre')


class MovieUpdateView(UpdateView):
    model = Genre
    form_class = GenreCreateForm
    template_name = 'info_genre.html'
    success_url = reverse_lazy('movies_app:list_genre')
