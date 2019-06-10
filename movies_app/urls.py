from django.urls import path
from . import views

app_name = 'movies_app'
urlpatterns = [
    path('list_genre',views.GenreListView.as_view(),name='list_genre'),
    path('create_genre',views.GenreCreateView.as_view(),name='create_genre'),
    path('update_genre/<pk>',views.GenreUpdateView.as_view(),name='update_genre'),

    path('list_movie',views.MovieListView.as_view(),name='list_movie'),
    path('create_movie',views.MovieCreateView.as_view(),name='create_movie'),
    path('update_movie/<pk>',views.MovieUpdateView.as_view(),name='update_movie'),

    ]