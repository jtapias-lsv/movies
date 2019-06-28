from celery import chord, group
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.views import View
from django.views.generic import ListView, CreateView, UpdateView, DetailView, FormView
from django.urls import reverse_lazy
from django.views.generic.list import BaseListView
from rest_framework.generics import RetrieveAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.authtoken.models import Token
#from rest_framework_xml.renderers import XMLRenderer
#import time


from django.core.management import call_command


from movies_app.tasks import donwload_movie, send_email
from .models import Genre, Movie, Rate, ValidatorToken
from .forms import GenreCreateForm, MovieCreateForm, SimpleForm, MyLoginForm, SimpleForm2, MyDownLoadForm

from movies_app.api.serializers import MovieOwnSerializerList, MovieOwnSerializerDetail, MovieSerializerCreateList, \
    MovieSerializerDetailUpdateDelete, MovieRateSerializer

from  rest_framework.renderers import JSONRenderer


class HomeView(ListView):
    template_name = 'home.html'
    extra_context = {'title':'My Internet Movie DataBase'}
    queryset = Movie.objects.all()
    paginate_by = 6

    def get_queryset(self):
        qs  = super(HomeView,self).get_queryset()
        return qs.order_by('-id')

    def get_context_data(self, **kwargs):
        data = super(HomeView,self).get_context_data(**kwargs)
        #data.update({'titulo':'Mi Propio Internet de Peliculas'})
        best_movie = Rate.objects.get_best_rated().first()
        if best_movie:
            movie = Movie.objects.get(pk=best_movie.get('movie'))
            data.update({
                'best_rated_movie' : movie,
                'best_rated_value' : best_movie.get('rate',0)
            })
            return data



class MovieDetailView(LoginRequiredMixin, DetailView):
    queryset = Movie.objects.all()
    template_name = 'detail.movie.html'
    slug_field = 'slug'
    query_pk_and_slug = False




class MovieFormExample(CreateView):
    template_name = 'simple.form.example.html'
    form_class = SimpleForm2
    success_url = reverse_lazy('movies_app:home')

    def form_invalid(self, form):
        print(form.errors)
        return super(MovieFormExample, self).form_invalid(form)

    def get_form_kwargs(self):
        kwargs = super(MovieFormExample, self).get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs

    #def form_valid(self, form):
    #    pass

class MyDownLoadView(View):

    def __init__(self):
        self.template_name = 'download.html'
        self.form_class = MyDownLoadForm

    def get(self, request, *args, **kwargs ):
        return render(request, self.template_name, {'form':self.form_class})

    def post(self, request):
        my_form = MyDownLoadForm(request.POST)
        if my_form.is_valid():
            my_titles = my_form.cleaned_data['title_movie']
            my_reciver = my_form.cleaned_data['reciver_mail']
            my_list_movie = my_titles.split(", ")
            temp_signature = []
            for mov in my_list_movie:
                temp_signature.append(donwload_movie.s(mov))

            chord(group(*temp_signature))(send_email.s(my_reciver))

        return HttpResponseRedirect(reverse_lazy('movies_app:download'))


class MyLoginView(View):

    def __init__(self):
        self.template_name = 'login.html'
        self.form_class = MyLoginForm

    def get(self, request ,*argv , **kwargs):
        return render(request,self.template_name,{'form':MyLoginForm})

    def post(self, request):
        my_form = MyLoginForm(request.POST)
        if my_form.is_valid():
            my_user = my_form.cleaned_data['username']
            my_pass = my_form.cleaned_data['password']
            the_user = authenticate(username = my_user, password=my_pass)
            Token.objects.update_or_create(user=my_user)
            if the_user is not None:
                login(request,the_user)
                if not ValidatorToken.objects.filter(user=the_user).exists():
                    vt = ValidatorToken()
                    vt.user = the_user
                    donwload_movie.delay()
                    vt.save()

                return HttpResponseRedirect(reverse_lazy('movies_app:home'))
        return HttpResponse('logeo fallido')




class MyLogoutView(View):

    def get(self,request):
        my_id = request.user
        Token.objects.get(user=my_id).delete()
        #ValidatorToken.objects.get(user=my_id).delete()
        logout(request)
        return HttpResponseRedirect(reverse_lazy('mylogin'))



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



class MyMoviesListView(BaseListView):

    model = Movie
    content_type = 'application/json'
    #content_type = 'text/xml'
    response_class = HttpResponse


    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(MyMoviesListView,self).get_context_data(object_list=object_list,**kwargs)
        #context.update({'serialized_data': XMLRenderer().render(MovieSerializerList(self.get_queryset(), many=True).data)})
        context.update({'serialized_data': JSONRenderer().render(MovieOwnSerializerList(self.get_queryset(),many=True).data)})
        return context

    def render_to_response(self, context, **response_kwargs):
        response_kwargs.setdefault('content_type', self.content_type)
        return self.response_class(
            context.get('serialized_data'), **response_kwargs #content_type=self.content_type
        )




class MyMoviesDetailsView(DetailView):

    model = Movie
    content_type = 'application/json'
    response_class = HttpResponse

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(MyMoviesDetailsView, self).get_context_data(object_list=object_list, **kwargs)
        context.update({'serialized_data': JSONRenderer().render(MovieOwnSerializerDetail(self.get_object()).data)})
        return context

    def render_to_response(self, context, **response_kwargs):
        response_kwargs.setdefault('content_type', self.content_type)
        return self.response_class(
            context.get('serialized_data'), **response_kwargs
        )

    def get_object(self, queryset=None):

        try:
            peli = Movie.objects.get(slug=self.kwargs['slug'])
        except Movie.DoesNotExist as e:
            call_command('download', self.kwargs['slug'])

        if peli:
            return peli
    #self.kwargs
    #call_command('download', 'titanic')  # here I need pass the slug parameter

# ----------------------------------------------------------------------------------------------
class MovieRateDetailView(RetrieveAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieRateSerializer
    lookup_field = 'slug'


class MovieCreateListView(ListCreateAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializerCreateList

class MovieDetailUpdateDeleteView(RetrieveUpdateDestroyAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializerDetailUpdateDelete
    lookup_field = 'slug'
