from utils.http_response import *


def login_required(func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated():
            return auth_required()
        return func(request, *args, **kwargs)
    return wrapper
