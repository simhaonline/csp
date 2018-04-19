import json
import time

from django.core import serializers
from utils.http_response import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from geopy.geocoders import Nominatim


from cstasker.models import UserTask, Task, LockRecord, PeriodicalRecord, Photo
from utils.auth import login_required
from utils.http_response import *

import cstasker.task as celery_task


@csrf_exempt
@login_required
def self_create_task(request):
    user = request.user
    celery_task.gen_task_for_user(user)
    return success()


@login_required
def get_task_list(request):
    user = request.user
    tasks = list(UserTask.objects.filter(user=user, status__in=[0, 2]).values())
    for t in tasks:
        t['task'] = Task.objects.filter(id=t['task_id']).values()[0]
    # print(tasks)
    return JsonResponse(tasks)


@csrf_exempt
@login_required
def get_task(request, task_id):
    print(task_id)
    task = list(UserTask.objects.filter(ut_id=int(task_id)).values())
    if len(task) > 0:
        return JsonResponse(task[0])
    else:
        return runtime_error("no such id")


@csrf_exempt
@login_required
def handle_lock_record(request):
    action = request.POST.get('action', -1)
    record = LockRecord(timestamp=int(time.time()), user=request.user, action=action)
    record.save()
    return success()


@csrf_exempt
@login_required
def user_finish_task(request):
    print(request.user)
    if 'image' in request.FILES:
        image = request.FILES["image"]
        title = request.POST.get('title', '')
        photo = Photo(image=image, title=title)
        photo.save()
    else:
        return runtime_error(content='image not found')
    return success(content='任务成功提交')


@csrf_exempt
@login_required
def user_modify_task_status(request):
    status = int(request.POST.get('status', -1))
    task_id = int(request.POST.get('taskId', -1))
    if status > 0 and task_id > 0:
        task = UserTask.objects.filter(ut_id=task_id, user=request.user)
        if len(task) > 0:
            if status is 5:
                if task[0].status is 2:
                    task[0].status = status
                    task[0].save()
                    return success("状态修改成功")
                else:
                    return runtime_error("状态不合法")
            else:
                task[0].status = status
                task[0].save()
                return success("状态修改成功")
    return runtime_error("没有相应的任务")


@csrf_exempt
@login_required
def handle_periodical_record(request):
    latitude = int(request.POST.get('latitude', 0))
    longitude = int(request.POST.get('longitude', 0))
    location = ''
    if longitude != 0 and latitude != 0:
        geolocator = Nominatim()
        location = geolocator.reverse("{},{}".format(latitude, longitude)).address
    record = PeriodicalRecord(timestamp=int(time.time()), user=request.user, latitude=latitude,
                              longitude=longitude, poi=location)
    record.save()
    return success()
