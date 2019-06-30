import os
from celery import Celery
from celery.schedules import crontab

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'movies.settings')

# app = Celery('movies', backend='amqp://guest:guest@localhost:5672//',)
app = Celery('movies', backend='django-db://',)


# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()


app.conf.beat_schedule = {
    'dowload-sugestion-every-10-minutes': {
        'task': 'movies_app.tasks.movie_suggestion',
        'args': (),
        'schedule': crontab(minute='*/3'),
    },
}
app.conf.timezone = 'UTC'


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))


