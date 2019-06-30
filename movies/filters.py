import django_filters


class MovieFilterset(django_filters.FilterSet):
    """ It allows to make filters in searchs """


    title = django_filters.CharFilter(lookup_expr='icontains')
    """ if this field match with a module's name propertie, is not necesary to put field_name atribute"""

    year = django_filters.NumberFilter(field_name='release_date', lookup_expr='year')
    realease_date = django_filters.DateFromToRangeFilter()
