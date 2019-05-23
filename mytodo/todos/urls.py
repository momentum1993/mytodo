from django.urls import path
# from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required

from . import views

app_name = 'todos' # 다른 어플과의 URL 중복을 피하기 위해 네임 스페이스 생성해줌.
urlpatterns = [
    path('', views.index, name='index'), # 메인 페이지
    path('<int:pk>/', login_required(views.DetailView.as_view()), name='detail'), # 세부적인 todo 페이지
    path('<int:todo_id>/check/', views.check_todo, name='check'), # sub todo의 체크 여부 확인
    path('<int:todo_id>/done/', views.done, name='done'), # todo가 모두 완료되었는지 확인
    path('write/', views.write_todo, name='write'), # todo 작성
    path('<int:todo_id>/edit/', views.edit_todo, name='edit'), # todo 수정
    path('<int:todo_id>/delete/', views.delete_todo, name='delete'), # todo 삭제
    path('accounts/login/', views.account_login, name='login'), # 웹페이지 로그인
    path('accounts/logout/', views.account_logout, name='logout'), # 웹페이지 로그아웃
    path('accounts/signup/', views.account_signup, name='signup'), # 웹페이지 회원가입
]