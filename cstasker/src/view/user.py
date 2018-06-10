from django.contrib.auth import authenticate, login, logout
# from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render
import base64


# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser

from cstasker.models import Person, Photo, UserTask, UserProfile
from cstasker.serialize import PersonSerializer
from utils.auth import login_required
from utils.utils import *
from utils.http_response import *

import cstasker.task as celery_task
from djcelery.models import PeriodicTask, CrontabSchedule


@login_required
def hello(request):
    # celery_task.hello.delay()
    # schedule, _ = CrontabSchedule.objects.create(
    #
    # )
    # PeriodicTask.objects.create(
    #
    # )
    return HttpResponse('hello')


def test(request):
    # celery_task.gen_task_for_all()
    celery_task.gen_questionnaire_for_all()
    # send_notification('您收到了新的任务')
    # celery_task.finish_user_questionnaire(201805114114869)
    return HttpResponse("test")


@login_required
def get_user_info(request):
    user_profile = UserProfile.objects.filter(user=request.user).values()
    if len(user_profile) > 0:
        print(user_profile)
        user_profile[0]['user_name'] = request.user.username
        user_task = UserTask.objects.filter(user=request.user, status=3).values()
        user_profile[0]['finish_count'] = len(user_task)
        return JsonResponse(user_profile[0])
        # return success(content=request.user.username)
    else:
        return runtime_error(content='用户不存在')


@csrf_exempt
def user_login(request):
    username = request.POST.get('username', None)
    password = request.POST.get('password', None)
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            # print(user.id)
            login(request, user)
            return JsonResponse({'id': user.id, 'name': user.username})
            # return success(content='login success')
            # Redirect to a success page.
        else:
            return runtime_error(content='disable account')
            # Return a 'disabled account' error message
    else:
        # Return an 'invalid login' error message.
        return runtime_error(content='invalid login')


def log_out(request):
    logout(request)
    return success()


@csrf_exempt
def create_user(request):
    username = request.POST.get('username', None)
    password = request.POST.get('password', None)
    print((username, password))
    if username and password:
        if len(User.objects.filter(username=username)) > 0:
            return runtime_error(content='user name has been used')
        user = User.objects.create_user(username=username, password=password)
        user.save()
        user_profile = UserProfile(user=user, score=0)
        user_profile.save()
        return success(user.username)
        # data = JSONParser().parse(request)
        # person = PersonSerializer(data=data)
        # if person.is_valid():
        #     person.save()
        #     return success(person.data)
    else:
        return runtime_error(content='must input username and password')


def get_all_user(request):
    all_users = User.objects.all()
    return success(content=all_users[0].password)


