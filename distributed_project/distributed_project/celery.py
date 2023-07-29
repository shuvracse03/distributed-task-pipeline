import os
from celery import Celery
from django.conf import settings

# set the default Django settings module for the 'celery' program.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "distributed_project.settings")

BROKER = "amqp://admin:pass123@rabbit:5672/myvhost"

app = Celery("distributed_project", broker=BROKER)


app.config_from_object("django.conf:settings")

# Load task modules from all registered Django app configs...
app.autodiscover_tasks(settings.INSTALLED_APPS)

#For debug
@app.task(bind=True)
def debug_task(self):
    print(f"Request: {self.request!r}")
