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

from cstasker.models import Person, Photo
from cstasker.serialize import PersonSerializer
from utils.auth import login_required
from utils.http_response import *

import cstasker.task as celery_task


# @login_required
def hello(request):
    celery_task.hello.delay()
    return HttpResponse('123')


@csrf_exempt
def user_login(request):
    username = request.POST.get('username', None)
    password = request.POST.get('password', None)
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            login(request, user)
            return success(content='login success')
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


@login_required
def user_get_task(request):
    print(request.user)
    return success(content=request.user.username)


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
