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


class UserInfo(models.Model):
    user = models.ForeignKey(User)
    score = models.IntegerField()

    def __str__(self):
        return '{},{}'.format(self.user, self.score)


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

QUESTIONNAIRE_STATUS = (
    (0, 'Published'),
    (1, 'Finished'),
    (2, 'Expired'),
)


class Record(models.Model):
    timestamp = models.IntegerField()
    user = models.ForeignKey(User)


class UserTask(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    publish_time = models.DateTimeField(blank=True, null=True)
    action_time = models.DateTimeField(blank=True, null=True)
    start_time = models.DateTimeField(blank=True, null=True)
    end_time = models.DateTimeField(blank=True, null=True)
    status = models.IntegerField(choices=TASK_STATUS, null=True)
    ut_id = models.BigIntegerField(primary_key=True)

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


class LockRecord(models.Model):
    id = models.AutoField(primary_key=True)
    timestamp = models.IntegerField(blank=True, null=True)
    user = models.ForeignKey(User)
    action = models.IntegerField()


class PeriodicalRecord(models.Model):
    id = models.AutoField(primary_key=True)
    timestamp = models.IntegerField(blank=True, null=True)
    user = models.ForeignKey(User)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    poi = models.TextField(max_length=255, null=True, blank=True)
    net_info = models.IntegerField(blank=True, null=True)


class BatteryRecord(models.Model):
    id = models.AutoField(primary_key=True)
    timestamp = models.IntegerField(blank=True, null=True)
    user = models.ForeignKey(User)
    level = models.FloatField(blank=True, null=True)
    charge = models.IntegerField(blank=True, null=True)


class Questionnaire(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.TextField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.name


class Question(models.Model):
    id = models.AutoField(primary_key=True)
    questionnaire = models.ForeignKey(Questionnaire, on_delete=models.CASCADE)
    description = models.TextField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.description


class QuestionOption(models.Model):
    id = models.AutoField(primary_key=True)
    q_id = models.ForeignKey(Question, on_delete=models.CASCADE)
    content = models.TextField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.content


class UserQuestionnaire(models.Model):
    questionnaire = models.ForeignKey(Questionnaire, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    publish_time = models.DateTimeField(blank=True, null=True)
    action_time = models.DateTimeField(blank=True, null=True)
    start_time = models.DateTimeField(blank=True, null=True)
    end_time = models.DateTimeField(blank=True, null=True)
    status = models.IntegerField(choices=QUESTIONNAIRE_STATUS, null=True)
    uq_id = models.BigIntegerField(primary_key=True)


class UserChoice(models.Model):
    id = models.AutoField(primary_key=True)
    questionnaire = models.ForeignKey(Questionnaire, null=True, blank=True, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    uq = models.ForeignKey(UserQuestionnaire, on_delete=models.CASCADE, null=True, blank=True)
    user_choice = models.IntegerField(null=True, blank=True)


class UserProfile(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User)
    tel = models.TextField(max_length=11, null=True, blank=True)
    email = models.TextField(max_length=128, null=True, blank=True)
    score = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.user.username


class Canteen(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.TextField(max_length=32, null=True, blank=True)

    def __str__(self):
        return self.name


class CanteenLog(models.Model):
    id = models.AutoField(primary_key=True)
    canteen = models.ForeignKey(Canteen)
    ip_count = models.IntegerField(null=True, blank=True)
