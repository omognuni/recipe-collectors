from celery import shared_task

from datetime import datetime


@shared_task
def print_time():
    print("print time:", datetime.now())
