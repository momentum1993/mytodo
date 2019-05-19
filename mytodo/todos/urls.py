from django.urls import path

from . import views

app_name = 'todos' # 다른 어플과의 URL 중복을 피하기 위해 네임 스페이스 생성해줌.
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('<int:todo_id>/check/', views.check_todo, name='check'),
    path('<int:todo_id>/done/', views.done, name='done'),
    path('write/', views.write_todo, name='write'),
    path('<int:todo_id>/edit/', views.edit_todo, name='edit'),
    path('<int:todo_id>/delete/', views.delete_todo, name='delete'),
]