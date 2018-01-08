from utils.http_response import *


def login_required(func):
    def wrapper(request):
        if not request.user.is_authenticated():
            return auth_required()
        return func(request)
    return wrapper
