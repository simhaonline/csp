from django.contrib.auth.models import User
from django.db import models
# Create your models here.


class Person(models.Model):
    first_name = models.CharField(max_length=40)
    last_name = models.CharField(max_length=40)

    def __str__(self):
        return '{} {}'.format(self.first_name, self.last_name)


TASK_TYPE = (
    (0, 'LocationBased'),
)


class Task(models.Model):
    type = models.IntegerField(choices=TASK_TYPE)
    title = models.CharField(max_length=60)
    content = models.TextField()
    extra_data = models.TextField(blank=True)

    def __str__(self):
        return self.title


TASK_STATUS = (
    (0, 'Published'),
    (1, 'Refused'),
    (2, 'Accepted'),
    (3, 'Finish'),
    (4, 'UnFinish'),
)


class Record(models.Model):
    timestamp = models.TimeField()
    user = models.ForeignKey(User)


class UserTask(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    publish_time = models.TimeField(blank=True, null=True)
    action_time = models.TimeField(blank=True, null=True)
    start_time = models.TimeField(blank=True, null=True)
    end_time = models.TimeField(blank=True, null=True)
    status = models.IntegerField(choices=TASK_STATUS, null=True)

    def __str__(self):
        return '{}_{}_{}'.format(self.user, self.task, self.status)


class Photo(models.Model):
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='photos')

    def __str__(self):
        return self.title


class GPSRecord(Record):
    latitude = models.FloatField()
    longitude = models.FloatField()
    poi = models.TextField()


class MovingRecord(Record):
    speed = models.FloatField()
