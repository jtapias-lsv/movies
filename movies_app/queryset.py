from django.db.models import QuerySet, Sum, Count, FloatField


class MovieQuerySet(QuerySet):
    """define movies for years"""

    def get_by_year(self, year=None):
        if year:
            return self.filter(release_date__year=year)
        else:
            return self


class MovieRateQuerySet(QuerySet):
    """define a set of searches"""

    def get_best_rated(self):
        return self.values('movie').annotate(#movie__slug
            rate=Sum('rate', output_field=FloatField()) / Count('movie', output_field=FloatField())).order_by('-rate')

    def get_for_movie(self, movie):
        return self.filter(movie=movie)

    def get_rate_movie(self,movie):
        return self.get_for_movie(movie).get_best_rated


class LoginQuerySet(QuerySet):

    def get(self, username, password):
        return self.filter()