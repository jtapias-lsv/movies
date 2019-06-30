from rest_framework import serializers

from movies_app.models import Movie, Rate


class MovieOwnSerializerList(serializers.Serializer):
    """ To serialize movies for rest_framework and give information in a list"""

    title = serializers.CharField()
    rate = serializers.SerializerMethodField()
    """ this field look for a function named: get_rate """

    def get_rate(self, obj):
        """
        if function is named <get_+field name>, it will call automatically
        Args:
            obj: necesary to make filter

        Returns: empty string

        """
        rate = Rate.objects.filter(movie__pk=obj.id)
        if rate.exists():
            return rate.get_best_rated().first()['rate']

        return ''


class MovieOwnSerializerDetail(serializers.Serializer):
    """ Showing more information in detail """

    title = serializers.CharField()
    detail = serializers.CharField()
    release_date = serializers.DateField(input_formats=['%d/%m/%Y'])
    duration = serializers.IntegerField()


# ------------------WORKING WITH MODELSERIALIZER---------------------------------------------

class MovieSerializer(serializers.ModelSerializer):
    """To show movie information"""

    pk = serializers.IntegerField(source='id')
    poster = serializers.ImageField(read_only=True)
    trailer_url = serializers.URLField(required=False)

    class Meta:
        model = Movie
        fields = ('title', 'duration', 'poster', 'detail',
                  'trailer_url', 'genre', 'original_language',
                  'country', 'release_date','pk')


class MovieRateSerializer(serializers.ModelSerializer):
    """To show rate information"""

    pk = serializers.IntegerField(source='id',read_only=True)
    user = serializers.StringRelatedField()
    movie = MovieSerializer(read_only=True)
    #id = serializers.HyperlinkedIdentityField(view_name='api-movies_app:movierate-detail-actions')
    # movie_link = serializers.HyperlinkedRelatedField(source='movie', read_only=True,
    #                                                  view_name='movies_app:movie-de-up-de',

    #                                                  lookup_field='slug')

    class Meta:
        model = Rate
        fields = ('movie', 'user', 'pk', 'rate')




class MovieSerializerCreateList(serializers.ModelSerializer):
    """To allow create new movie and list the storage movies, through the API """

    link = serializers.HyperlinkedIdentityField(read_only=True, view_name='movies_app:movie-de-up-de',
                                                lookup_field='slug')

    class Meta:
        model = Movie
        fields = (
            'title', 'duration', 'poster', 'about', 'detail', 'trailer_url', 'genre', 'original_language',
            'release_date',
            'country', 'slug', 'link')




class MovieSerializerDetailUpdateDelete(serializers.ModelSerializer):
    """To allow update, show datails an delete a movie through the API """

    class Meta:
        model = Movie
        fields = ('id','title','duration','detail','poster')




class MovieRateSerializer2(serializers.ModelSerializer):
    """This class is for make an nested serialized example"""

    id = serializers.HyperlinkedIdentityField(view_name='api-movies_app:movierate-detail-actions')
    user = serializers.StringRelatedField()
    movie_link = serializers.HyperlinkedRelatedField(source='movie', read_only=True,
                                                     view_name='api-movies_app:movie-detail-actions',
                                                     lookup_field='pk')

    movie = MovieOwnSerializerList(read_only=True)
    """property read_only for don't show the movie creation form"""

    class Meta:
        model = Rate
        fields = ('movie', 'user', 'rate', 'id', 'movie_link', 'pk')


