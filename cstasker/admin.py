from django.contrib import admin

# Register your models here.
from cstasker.models import *

admin.site.register(Person)
admin.site.register(Task)
admin.site.register(UserTask)
admin.site.register(Photo)
