import json

from django.core import serializers
from django.views.decorators.csrf import csrf_exempt
from djcelery.views import JsonResponse

from cstasker.models import UserTask, Task
from utils.auth import login_required
from utils.http_response import *

import cstasker.task as celery_task


@csrf_exempt
@login_required
def self_create_task(request):
    user = request.user
    celery_task.gen_task_for_user(user)
    return success()


@csrf_exempt
@login_required
def get_task_list(request):
    user = request.user
    tasks = list(UserTask.objects.filter(user=user).values())
    return JsonResponse(tasks)
