from django.contrib import admin

# Register your models here.
from cstasker.models import *


class UserTaskAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'task_id', 'publish_time', 'end_time', 'status')
    list_display_links = ('user_id', 'task_id')


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'tel', 'email', 'score')
    list_display_links = 'user'


admin.site.register(Person)
admin.site.register(Task)
admin.site.register(UserTask, UserTaskAdmin)
admin.site.register(Photo)
admin.site.register(UserProfile)
admin.site.register(Questionnaire)
admin.site.register(Question)
admin.site.register(Canteen)
admin.site.register(CanteenLog)
