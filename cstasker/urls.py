from django.conf.urls import url
from cstasker.src.view import user, task

urlpatterns = [
    url(r'^user/hello', user.hello),
    url(r'^user/test', user.test),
    url(r'^user/create', user.create_user),
    url(r'^user/login', user.user_login),
    url(r'^user/logout', user.log_out),
    url(r'^user/info', user.get_user_info),
    url(r'^user/user/list', user.get_all_user),
    url(r'^user/task/finish', task.user_finish_task),
    url(r'^task/lock_record', task.handle_lock_record),
    url(r'^user/task/(\d+)', task.get_task),
    url(r'^user/task/modify_status', task.user_modify_task_status),
    url(r'^user/task/self_create', task.self_create_task),
    url(r'^user/task/task_list', task.get_task_list),
]
