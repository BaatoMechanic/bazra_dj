import os
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "bazra_dj.settings.common")


celery = Celery("bazra_dj")

celery.config_from_object("django.conf:settings", namespace="CELERY")

celery.autodiscover_tasks()
