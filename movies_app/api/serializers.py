from rest_framework import serializers

from movies_app.models import Movie, Rate


class MovieOwnSerializerList(serializers.Serializer):

    title = serializers.CharField()
    release_date = serializers.DateField(input_formats=['%d/%m/%Y'])
    duration = serializers.IntegerField()
    rate = serializers.SerializerMethodField() # busca la funcion get_rate

    # lo busca porque la funcion se llama get_ y nombre del campo
    def get_rate(selfself, obj):
        rate=Rate.objects.filter(movie__pk=obj.id)
        if rate.exists():
            return rate.get_best_rated().first()['rate']

        return ''


class MovieOwnSerializerDetail(serializers.Serializer):
    title = serializers.CharField()
    detail = serializers.CharField()

# -------------------------------------------------------------------------------

class MovieSerializer(serializers.ModelSerializer):

    pk = serializers.IntegerField(source='id')
    poster = serializers.ImageField(read_only=True)
    trailer_url = serializers.URLField(required=False)

    class Meta:
        model = Movie
        fields = ('title', 'duration', 'poster', 'detail',
                  'trailer_url', 'genre', 'original_language',
                  'country', 'release_date','pk')


class MovieRateSerializer(serializers.ModelSerializer):

    pk = serializers.IntegerField(source='id',read_only=True)
    #id = serializers.HyperlinkedIdentityField(view_name='api-movies_app:movierate-detail-actions')
    user = serializers.StringRelatedField()
    # movie_link = serializers.HyperlinkedRelatedField(source='movie', read_only=True,
    #                                                  view_name='movies_app:movie-de-up-de',
    #                                                  lookup_field='slug')

    movie = MovieSerializer(read_only=True)

    class Meta:
        model = Rate
        fields = ('movie', 'user', 'pk', 'rate')




class MovieSerializerCreateList(serializers.ModelSerializer):

    link = serializers.HyperlinkedIdentityField(read_only=True, view_name='movies_app:movie-de-up-de', lookup_field='slug')

    class Meta:
        model = Movie
        fields = (
            'title', 'duration', 'poster', 'about', 'detail', 'trailer_url', 'genre', 'original_language',
            'release_date',
            'country', 'slug', 'link')




class MovieSerializerDetailUpdateDelete(serializers.ModelSerializer):

    class Meta:
        model = Movie
        fields = ('id','title','duration','detail','poster')


class MovieRateSerializer2(serializers.ModelSerializer):

    id = serializers.HyperlinkedIdentityField(view_name='api-movies_app:movierate-detail-actions')
    user = serializers.StringRelatedField()
    movie_link = serializers.HyperlinkedRelatedField(source='movie', read_only=True,
                                                     view_name='api-movies_app:movie-detail-actions',
                                                     lookup_field='pk')
    # read only para que no se muestre el formulario de creacion de movie
    movie = MovieOwnSerializerList(read_only=True)

    class Meta:
        model = Rate
        fields = ('movie', 'user', 'rate', 'id', 'movie_link', 'pk')


