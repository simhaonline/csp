from django.http import HttpResponse


def success(content='success'):
    return HttpResponse(status=200, content=content)


def runtime_error(content='something wrong'):
    return HttpResponse(status=400, content=content)


def auth_required(content='auth required'):
    return HttpResponse(status=401, content=content)

