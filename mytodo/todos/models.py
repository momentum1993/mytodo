from django.db import models
from django.utils import timezone
from datetime import datetime

class Todo(models.Model):

    title = models.CharField(max_length=200)
    priority = models.IntegerField(default=0)
    pub_date = models.DateTimeField('date published')
    due_date = models.DateTimeField('due date')
    all_done = models.BooleanField(default=False)

    class Meta:
        ordering = ['priority']

    def __str__(self):
        return self.title

    def is_overdue(self):
        return True if self.due_date < timezone.now().replace(microsecond=0) else False

    def left_time(self):
        return timezone.now().replace(microsecond=0) - self.due_date

class Specific_todo(models.Model):
    todo = models.ForeignKey(Todo, on_delete=models.CASCADE)
    content = models.CharField(max_length=200)
    is_checked = models.BooleanField(default=False)

    def __str__(self):
        return self.todo.title + ': ' + self.content

class Done(models.Model):
    todo = models.OneToOneField(Todo, on_delete=models.CASCADE)
    done_date = models.DateTimeField('date that todo is done')

    def __str__(self):
        return self.todo.title


# Create your models here.

#모델을 변경할 때에는
# 1. models.py에서 모델을 변경
# 2. python manage.py makemigrations를 통해 변경사항에 대한 migration 생성
# 3. python manage.py migrate 명령을 통해 변경사항을 데이터베이스에 적용.
