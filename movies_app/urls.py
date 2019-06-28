from django.urls import path
from . import views

app_name = 'movies_app'
urlpatterns = [
    path('list_genre',views.GenreListView.as_view(),name='list_genre'),
    path('create_genre',views.GenreCreateView.as_view(),name='create_genre'),
    path('update_genre/<pk>',views.GenreUpdateView.as_view(),name='update_genre'),
    path('', views.HomeView.as_view(), name='home'),
    path('movies/<slug>/', views.MovieDetailView.as_view(), name='movie_detail'),
    path('form/', views.MovieFormExample.as_view(),name='simple_form'),
    path('api_list/',views.MyMoviesListView.as_view(),name='api_list'),
    path('api_detail/<slug>',views.MyMoviesDetailsView.as_view(),name='api_detail'),

    path('movie/',views.MovieCreateListView.as_view(),name='movie-li-cre'),
    path('movie/<slug>',views.MovieDetailUpdateDeleteView.as_view(),name='movie-de-up-de'),
    path('download',views.MyDownLoadView.as_view(), name='download'),

    ]