from django import forms
from django.contrib.auth.models import User

class TodoForm(forms.Form): # Todo 작성, 수정 시 이용할 form
    title = forms.CharField(max_length=200, widget=forms.Textarea)  # title
    priority = forms.IntegerField() # 우선순위
    due_date = forms.DateTimeField(input_formats = ["%Y-%m-%dT%H:%M"],
        widget = forms.DateTimeInput(
            attrs={
                'type': 'datetime-local',
                'class': 'form-control'},
            format='%Y-%m-%dT%H:%M')) # 만료시각
    sub_todos = forms.CharField(widget=forms.Textarea) #세부 todos

class LoginForm(forms.Form): # 로그인 시 이용할 form
    username = forms.CharField(min_length=4,max_length=20, widget=forms.Textarea) # username
    password = forms.CharField(min_length=6, max_length=20, widget=forms.PasswordInput) # password

class UserForm(forms.Form): #  회원가입 시 이용할 form
    username = forms.CharField(min_length=4, max_length=20, widget=forms.Textarea) #username
    email = forms.EmailField() # email
    password = forms.CharField(min_length=6,max_length=20, widget=forms.PasswordInput) # password
