import json
from datetime import datetime

from django.http import HttpResponse


def success(content='success'):
    return HttpResponse(status=200, content=content)


def runtime_error(content='something wrong'):
    return HttpResponse(status=400, content=content)


def auth_required(content='auth required'):
    return HttpResponse(status=401, content=content)


class DateTimeEncoder(json.JSONEncoder):
    # default JSONEncoder cannot serialize datetime.datetime objects
    def default(self, obj):
        if isinstance(obj, datetime):
            encoded_object = obj.strftime('%s')
        else:
            encoded_object = super(self, obj)
        return encoded_object


class JsonResponse(HttpResponse):
    def __init__(self, content, mimetype='application/json', status=None, content_type='application/json'):
        json_text = json.dumps(content, cls=DateTimeEncoder)
        super(JsonResponse, self).__init__(
            content=json_text,
            status=status,
            content_type=content_type)

