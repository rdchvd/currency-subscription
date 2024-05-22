import os

from celery import Celery
from celery.schedules import crontab

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "currency.settings")

app = Celery("currency")


app.config_from_object("django.conf:settings", namespace="CELERY")
app.conf.broker_transport_options = {"visibility_timeout": 345600}

app.autodiscover_tasks()
app.conf.beat_schedule = {
    "fetch_currency_data": {
        "task": "currencies.tasks.fetch_currency_data",
        "schedule": crontab(hour="7", minute="0"),
    },
}
