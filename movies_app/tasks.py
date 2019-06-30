from celery._state import get_current_app
from django.core.management import call_command
from celery import Task, chord, group
from django.core.mail import send_mail

from movies_app.models import Suggestion

app = get_current_app()

@app.task()
def add(x,y):
    print(x+y)
    return x+y


@app.task()
def send_email(p_body, p_reciver):
    send_mail(
        'Te enviamos la info',
        'Peliculas descargadas: '+str(p_body),
        'jtapias@lsv-tech.com',
        [p_reciver],
        #fail_silently=False
    )

@app.task()
def donwload_movie(title):
    """

    Args:
        title: movie tile to look for

    Returns: downloaded movie title

    """
    return call_command('download', title)


@app.task()
def delete_sugestion(p_id):
    Suggestion.objects.get(id=p_id).delete()


@app.task()
def movie_suggestion():

    movies = Suggestion.objects.all()

    if movies:
        temp_signature = []
        for mov in movies:
            temp_signature.append(donwload_movie.s(mov.title))
            delete_sugestion(mov.id)

        chord(group(*temp_signature))(send_email.s('jomitame@gmail.com'))


# ------------AN EXAMPLE WITH CLASS ----------------------

class MultiplyTask(Task):

    name = 'multiply_task'

    def run(self, x,y,*args,**kwargs):
        print(x*y)
        return x*y

app.register_task(MultiplyTask())