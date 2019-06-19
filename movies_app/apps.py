from django.apps import AppConfig


class MoviesAppConfig(AppConfig):
    name = 'movies_app'
    verbose_name = 'DjangoMovieDatabase'

    def ready(self):
        import movies_app.signals
    
