from celery import shared_task
from celery.task import periodic_task
from django.contrib.auth.models import User
from datetime import datetime, timedelta

from cstasker.models import Task, UserTask


@shared_task
def add(x, y):
    return x + y


@shared_task
def hello():
    print('hello celery')


@shared_task
def gen_task_for_user(user):
    print(user)
    task = Task.objects.filter(type=0)[0]
    # print(task)
    user_task = UserTask(task=task, user=user)
    user_task.save()


# @periodic_task(run_every=timedelta(seconds=10))
# def some_task():
#     print('periodic task starts')
