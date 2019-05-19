from django import forms
from django.contrib.auth.models import User

class TodoForm(forms.Form):
    title = forms.CharField(max_length=200, widget=forms.Textarea)
    priority = forms.IntegerField()
    due_date = forms.DateTimeField(input_formats = ["%Y-%m-%dT%H:%M"],
        widget = forms.DateTimeInput(
            attrs={
                'type': 'datetime-local',
                'class': 'form-control'},
            format='%Y-%m-%dT%H:%M'))
    sub_todos = forms.CharField(widget=forms.Textarea)

class LoginForm(forms.Form):
    username = forms.CharField(min_length=4,max_length=20, widget=forms.Textarea)
    password = forms.CharField(min_length=6, max_length=20, widget=forms.PasswordInput)

class UserForm(forms.Form):
    username = forms.CharField(min_length=4, max_length=20, widget=forms.Textarea)
    email = forms.EmailField()
    password = forms.CharField(min_length=6,max_length=20, widget=forms.PasswordInput)
