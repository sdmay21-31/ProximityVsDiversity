from celery import shared_task
from pathlib import Path
import os

from django.conf import settings


@shared_task
def touch_file():
    Path(os.path.join(settings.BASE_DIR, 'datasets', 'test')).touch()
