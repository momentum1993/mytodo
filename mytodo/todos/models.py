from django.db import models
from django.utils import timezone
from datetime import datetime
from django.contrib.auth.models import User

class Todo(models.Model): # Todo 모델
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None) # 유저필드이며, 해당 유저가 삭제되면 Todo도 연쇄적으로 삭제된다.
    title = models.CharField(max_length=200) # Todo 제목
    priority = models.IntegerField(default=0) # 우선순위
    pub_date = models.DateTimeField('date published') # Todo 생성시각
    due_date = models.DateTimeField('due date') # Todo 만료시각
    all_done = models.BooleanField(default=False) # Todo 안의 세부 todo가 다 완료 되었는지 여부 판별 플래그

    class Meta:
        ordering = ['priority'] # 우선순위를 기준으로 정렬

    def __str__(self): # 해당 모델 객체를 출력 시에 title로 출력
        return self.title

    def is_overdue(self): # 해당 모델 객체의 만료기간을 넘어갔을 경우 판별하는 함수
        return True if self.due_date < timezone.now().replace(microsecond=0) else False

    def left_time(self): # 해당 모델 객체가 만료시간까지 남은 시간을 반환해주는 함수
        return timezone.now().replace(microsecond=0) - self.due_date

class Specific_todo(models.Model): # 세부적인 Todo 모델
    todo = models.ForeignKey(Todo, on_delete=models.CASCADE) # todo 필드이며, 상위 todo가 삭제될 경우 세부 todo도 연쇄적으로 삭제된다.
    content = models.CharField(max_length=200) # 세부 todo의 내용
    is_checked = models.BooleanField(default=False) # 세부 todo의 완료 여부 판별 플래그

    def __str__(self):
        return self.todo.title + ': ' + self.content # 해당 모델 객체 출력시 부모 todo와 세부 todo 내용을 출력

class Done(models.Model): # Done 모델
    todo = models.OneToOneField(Todo, on_delete=models.CASCADE) # todo와 1대1로 가질 수 있으며, Todo가  삭제되면 같이 삭제된다.
    done_date = models.DateTimeField('date that todo is done') # todo가 완료된 시점 필드

    def __str__(self): # Done 객체 출력의 경우 todo의 title을 출력해준다.
        return self.todo.title


# Create your models here.

#모델을 변경할 때에는
# 1. models.py에서 모델을 변경
# 2. python manage.py makemigrations를 통해 변경사항에 대한 migration 생성
# 3. python manage.py migrate 명령을 통해 변경사항을 데이터베이스에 적용.
