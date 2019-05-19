from django.urls import path
# from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required

from . import views

app_name = 'todos' # 다른 어플과의 URL 중복을 피하기 위해 네임 스페이스 생성해줌.
urlpatterns = [
    path('', views.index, name='index'),
    path('<int:pk>/', login_required(views.DetailView.as_view()), name='detail'),
    path('<int:todo_id>/check/', views.check_todo, name='check'),
    path('<int:todo_id>/done/', views.done, name='done'),
    path('write/', views.write_todo, name='write'),
    path('<int:todo_id>/edit/', views.edit_todo, name='edit'),
    path('<int:todo_id>/delete/', views.delete_todo, name='delete'),
    path('accounts/login/', views.account_login, name='login'),
    path('accounts/logout/', views.account_logout, name='logout'),
    path('accounts/signup/', views.account_signup, name='signup'),
]