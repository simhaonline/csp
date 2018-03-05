from django.conf.urls import url
from cstasker.src.view import user, task

urlpatterns = [
    url(r'^user/hello', user.hello),
    url(r'^user/create', user.create_user),
    url(r'^user/login', user.user_login),
    url(r'^user/logout', user.log_out),
    url(r'^user/user/list', user.get_all_user),
    url(r'^user/task/list', user.user_get_task),
    url(r'^user/task/finish', user.user_finish_task),
    url(r'^user/task/self_create', task.self_create_task),
    url(r'^user/task/task_list', task.get_task_list),
]
