from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ValidationError

from .models import Genre, Movie, Rate


class GenreCreateForm(forms.ModelForm):

    class Meta:
        model = Genre
        fields = ('name','description')


class MovieCreateForm(forms.ModelForm):

    class Meta:
        model = Movie
        fields = '__all__'


def is_too_easy(value):
    if value == '1234':
        raise ValidationError('Is too easy')
    return value


class SimpleForm(forms.Form):
    password = forms.CharField(max_length=15,validators=[is_too_easy,])
    password2 = forms.CharField(max_length=15)


class MyLoginForm(forms.Form):

    username = forms.CharField( label = 'username' ,max_length=100)
    password = forms.CharField(label = 'password' ,max_length=100,
            widget=forms.PasswordInput)


class SimpleForm2(forms.ModelForm):

    rate = forms.IntegerField()

    class Meta:
        model = Rate
        fields = ('rate', 'movie', 'comment')

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(SimpleForm2, self).__init__(*args, **kwargs)

    def clean(self):
        data = super(SimpleForm2, self).clean()
        movie = data.get('movie')
        if Rate.objects.filter(user=self.user, movie=movie).exists():
            raise ValidationError(f'Movie rate with user {self.user.username} and movie {movie.title} already exists')
        return data

    def save(self, commit=True):
        instance = super(SimpleForm2, self).save(commit=False)
        instance.user = self.user
        instance.save()
        return instance



class MyDownLoadForm(forms.Form):

    title_movie = forms.CharField(label='Titulo', max_length=100)
    reciver_mail = forms.CharField(label='Email', max_length=100)


class MySuggestionForm(forms.Form):

    titles = forms.CharField(label='Sugerencias', max_length=100)