from django.contrib import admin

from .models import Todo, Specific_todo, Done

admin.site.register(Todo) # admin site에서 Todo 객체에 대해 관리할 수 있게 해준다.
admin.site.register(Specific_todo) # Specific_todo 객체 관리 가능
admin.site.register(Done) # Done 객체 관리 가능
# Register your models here.