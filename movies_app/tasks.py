from celery._state import get_current_app
from django.core.management import call_command
from celery import Task
from django.core.mail import send_mail

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
    my_string = call_command('download', title)
    return my_string



class MultiplyTask(Task):

    name = 'multiply_task'

    def run(self, x,y,*args,**kwargs):
        print(x*y)
        return x*y

app.register_task(MultiplyTask())