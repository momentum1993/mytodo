from django.contrib import admin

from .models import Todo, Specific_todo, Done

admin.site.register(Todo)
admin.site.register(Specific_todo)
admin.site.register(Done)
# Register your models here.