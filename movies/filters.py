import django_filters

class MovieFilterset(django_filters.FilterSet):
    # como este campo concuerde con el modelo no hay necesidad de poner file_name
    title = django_filters.CharFilter(lookup_expr='icontains')
    year = django_filters.NumberFilter(field_name='release_date', lookup_expr='year')
    realease_date = django_filters.DateFromToRangeFilter()