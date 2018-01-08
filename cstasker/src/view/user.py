from django.contrib.auth import authenticate, login, logout
# from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render


# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser

from cstasker.models import Person
from cstasker.serialize import PersonSerializer
from utils.auth import login_required
from utils.http_response import *


@login_required
def hello(request):
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
    # print((username, password))
    if username and password:
        user = User.objects.create_user(username=username, password=password)
        user.save()
        data = JSONParser().parse(request)
        person = PersonSerializer(data=data)
        if person.is_valid():
            person.save()
            return success(person.data)
    else:
        return runtime_error(content='must input username and password')
