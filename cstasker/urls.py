from django.conf.urls import url
from cstasker.src.view import user

urlpatterns = [
    url(r'^user/hello', user.hello),
    url(r'^user/create', user.create_user),
    url(r'^user/login', user.user_login),
    url(r'^user/logout', user.log_out),
]