import json
import time

from django.core import serializers
from utils.http_response import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from geopy.geocoders import Nominatim


from cstasker.models import UserTask, Task, LockRecord, PeriodicalRecord, Photo, UserQuestionnaire, Questionnaire, \
    Question, UserChoice, BatteryRecord, VoiceRecord, MovingRecord, AccRecord, AppUsageLog, BluetoothLog
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


@login_required
def get_questionnaire_list(request):
    user = request.user
    ques = list(UserQuestionnaire.objects.filter(user=user, status=0).values())
    for q in ques:
        q['qn'] = Questionnaire.objects.filter(id=q['questionnaire_id']).values()[0]
    return JsonResponse(ques)


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
def get_questionnaire(request, uq_id):
    user_questionnaire = list(UserQuestionnaire.objects.filter(uq_id=int(uq_id)).values())
    if (len(user_questionnaire)) > 0:
        uq = user_questionnaire[0]
        questions = list(Question.objects.filter(questionnaire_id=uq['questionnaire_id']).values("sort_key", "description"))
        questions = sorted(questions, key=lambda x: x['sort_key'], reverse=False)
        uq['questions'] = questions
        # print(questions)
        return JsonResponse(uq)
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
def handle_voice_data(request):
    score = request.POST.get('score')
    if score:
        voice_record = VoiceRecord(timestamp=int(time.time()), score=score, user=request.user)
        voice_record.save()
        return success()
    else:
        return runtime_error("no parameter score")


@csrf_exempt
@login_required
def handle_acc_data(request):
    ax = request.POST.get('ax')
    ay = request.POST.get('ay')
    az = request.POST.get('az')
    if ax and ay and az:
        record = AccRecord(user=request.user, timestamp=int(time.time()), ax=ax, ay=ay, az=az)
        record.save()
        return success()
    else:
        return runtime_error("parameter error")


@csrf_exempt
@login_required
def user_finish_task(request):
    if 'image' in request.FILES:
        image = request.FILES["image"]
        title = request.POST.get('title', '')
        photo = Photo(image=image, title=title)
        photo.save()
        latitude = request.POST.get('latitude', 0)
        longitude = request.POST.get('longitude', 0)
        task_id = int(request.POST.get('taskId', -1))
        task = UserTask.objects.filter(ut_id=task_id, user=request.user)
        if len(task) > 0:
            task[0].status = 3
            task[0].latitude = latitude
            task[0].longitude = longitude
            task[0].action_timestamp = int(time.time())
            task[0].photo = photo
            task[0].save()
            print(task[0].status)
            return success(content='任务成功提交')
        else:
            return runtime_error(content='no such user-task')
    else:
        return runtime_error(content='image not found')


@csrf_exempt
@login_required
def user_finish_questionnaire(request):
    option = request.POST.get('option', -1)
    uq_id = int(request.POST.get('uqId', -1))
    if option and uq_id >= 0:
        uq = UserQuestionnaire.objects.filter(uq_id=uq_id)
        if len(uq) > 0:
            uq[0].status = 1
            uq[0].action_timestamp = int(time.time())
            uq[0].save()
            # print(uq[0].questionnaire)
            choice = UserChoice(questionnaire=uq[0].questionnaire, user=uq[0].user, uq=uq[0], choices=option)
            choice.save()
            return success(content='问卷成功提交')
        return runtime_error(content='没有相应的任务')
    else:
        return runtime_error(content='问卷反馈失败')


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
                    task[0].action_timestamp = int(time.time())
                    task[0].save()
                    return success("状态修改成功")
                else:
                    return runtime_error("状态不合法")
            else:
                if status is 2:
                    task[0].start_timestamp = int(time.time())
                task[0].status = status
                task[0].save()
                return success("状态修改成功")
    return runtime_error("没有相应的任务")


@csrf_exempt
@login_required
def handle_periodical_record(request):
    latitude = float(request.POST.get('latitude', 0))
    longitude = float(request.POST.get('longitude', 0))
    level = float(request.POST.get('level', -1))
    charging = int(request.POST.get('charging', -1))
    net_info = int(request.POST.get('netInfo', -1))
    location = ''
    if longitude != 0 and latitude != 0:
        geolocator = Nominatim()
        location = geolocator.reverse("{},{}".format(latitude, longitude)).address
    b_record = BatteryRecord(timestamp=int(time.time()), user=request.user, level=level, charge=charging)
    b_record.save()
    record = PeriodicalRecord(timestamp=int(time.time()), user=request.user, latitude=latitude,
                              longitude=longitude, poi=location, net_info=net_info)
    record.save()
    return success()


@csrf_exempt
@login_required
def handle_app_log(request):
    user = request.user
    log = request.POST.get('log')
    if log:
        record = AppUsageLog(user=user, log=log, timestamp=int(time.time()))
        record.save()
        return success()
    else:
        return runtime_error('no log available')


@csrf_exempt
@login_required
def handle_bluetooth_log(request):
    user = request.user
    count = int(request.POST.get('count', 0))
    if count:
        record = BluetoothLog(user=user, timestamp=int(time.time()), scan_count=count)
        record.save()
        return success()
    else:
        return runtime_error('invalid count')
