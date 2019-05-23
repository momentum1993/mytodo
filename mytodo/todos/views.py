from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout

from .models import Todo, Specific_todo, Done
from .forms import TodoForm, LoginForm, UserForm
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User

def index(request):
    if request.user.is_authenticated: #로그인이 되어 있을 경우
        user = User.objects.get(username = request.user.username) # 해당 유저 객체를 갖고 온다.
        todo_list = user.todo_set.all() # 그리고 해당 유저가 가지는 Todo를 모두 갖고 온다.
        return render(request, 'todos/index.html', {'todo_list': todo_list }) # Http 요청과 해당 유저의 todo list들을 보내 렌더링해준다.
    else: # 로그인이 되어 있지 않은 경우
        return render(request, 'todos/login.html') # 로그인 화면으로 렌더링해준다.

class DetailView(generic.DetailView): # generic View를 이용하여 구현한 세부 todo 화면이다.
    model = Todo # 해당 Deatil view에 대해서 보낼 객체 모델은 todo 1개이다.
    template_name = 'todos/detail.html' # 그리고 해당 템플릿에 맞춰준다.

@login_required # 로그인이 되어야 쓸 수 있는 기능이다.
def check_todo(request, todo_id):
    todo = get_object_or_404(Todo, pk=todo_id) # id에 맞는 todo 객체를 가져오며, 없다면 404 error를 띄운다.
    checked_list = [] # 세부 todo 중에 체크된 것들만 모을 리스트이다.
    checked_list.extend(request.POST.getlist('sub_todo')) # POST방식으로 form에서 받은 sub_todo들(체크가 된 sub todo들)을 리스트에 추가해준다.
    all_sub_todos = todo.specific_todo_set.values('id') # 현재 todo에 있는 모든 sub_todo들의 id를 갖고 온다.
    for i in range(len(all_sub_todos)):
        checked_todo = todo.specific_todo_set.get(pk=all_sub_todos[i]['id']) #  sub todo의
        if str(checked_todo.id) in checked_list: # 체크된 sub todo의 id가 todo의 세부 todo 중에 하나라면
            checked_todo.is_checked = True # 체크됨에 True
        else: # 만약 아니라면
            checked_todo.is_checked = False # 체크가 되지 않지 않음.
        checked_todo.save() # 그리고 해당 sub todo를 저장한다.
    return HttpResponseRedirect(reverse('todos:done', args=(todo.id, ))) # 그리고 done에 대해서 실행하고 redirect 해준다.

@login_required # 로그인이 되어야 쓸 수 있는 기능
def done(request, todo_id):
    all_done = True
    todo = get_object_or_404(Todo, pk=todo_id) # todo의 id에 대해서 해당 todo를 갖고오고 실패하면 404를 띄운다.
    for i in todo.specific_todo_set.all(): # 해당 todo의  sub todo에 대해서
        if i.is_checked == False: # 만약 sub todo가 체크되어있지 않다면
            all_done = False # 나중에 done 여부 확인할 변수
            todo.all_done = False # todo객체의 all_done은 False가 되며
            todo.save() # 그값을 저장한다.
            try:
                d = Done.objects.get(todo=todo) # 그리고 해당 todo를 지니는 Done객체가 있다면
                d.delete() # 해당 done을 삭제한다.
                todo.done_date = None # 그리고 todo의 done_date도 비워준다.
                todo.save() # 해당 todo 저장
            except Done.DoesNotExist: # 만약 Done객체가 없다면
                pass # 그냥 패스
            break
    if all_done: # 만약 all_done이 True라면
        try:
            todo.done # todo에 대한 done객체가 있는지 확인하고
        except: # 아직 todo에 대한 done객체가 없을 때
            todo.all_done = True # 해당 todo의 all_done을 True로 해주고
            d = Done(todo=todo, done_date=timezone.now().replace(microsecond=0)) # 해당 todo에 연관된 새로운 Done객체를 생성한다.
            d.save() # 그리고 done 객체 저장.
            todo.save() # 그리고 해당 todo 객체 저장
    return render(request, 'todos/index.html', {'todo_list': User.objects.get(username=request.user.username).todo_set.all()})
    # 그리고 index 페이지를 띄워주는데, 해당 유저가 갖고있는 todo 객체만 넘긴다.

@login_required # 로그인이 되어야 쓸 수 있는 기능
def write_todo(request):
    if request.method == 'POST': # 만약 request가 POST 방식으로 들어왔다면
        form = TodoForm(request.POST) # Form.py의 TodoForm 객체를 일단 저장
        if form.is_valid(): # 만약 해당 form이 유효하다면
            todo = Todo(user=request.user, pub_date=timezone.now().replace(microsecond=0), due_date=form['due_date'].value(), title = form['title'].value(), priority = form['priority'].value(), all_done=False) #해당 form에서 쓴 내용에 맞춰 todo 객체를 만들어준다.
            todo.save() #그리고 만든 todo를 저장한다.
            for i in form.data.getlist('sub_todos'): # 그리고 form에서 얻은 sub todo들에 대해서
                sub_todo = Specific_todo(todo=todo, content=i, is_checked=False) # sub todo 객체 또한 생성해준다.
                sub_todo.save() # 그리고 sub todo 저장
            return HttpResponseRedirect('/') # 그리고 메인 index 페이지로 리다이렉트해준다.
    else: # 만약 form이 Post 방식으로 제대로 안넘어왔다면
        form = TodoForm() # 그냥 빈 todoForm을 넘긴다.
    return render(request, 'todos/write_todo.html', {'form': form,} ) # 그리고 해당 주소로 form과 함께 렌더링해준다.


@login_required # 로그인이 되어야 쓸 수 있는 기능
def edit_todo(request, todo_id):
    todo = Todo.objects.get(pk=todo_id)  # 해당 id에 대한 todo를 갖고온다.
    if request.method == 'POST': # 만약 request가 POST방식으로 넘어왔다면
        form = TodoForm(request.POST) # forms.py에 있는 TodoForm객체 형식으로 저장한다.
        if form.is_valid(): # 그리고 해당 form이 유효하다면
            todo.due_date =form['due_date'].value()
            todo.title = form['title'].value()
            todo.priority = form['priority'].value()
            todo.save() # 해당 todo안의 field들을 수정해주고 저장한다.

            sub_todo_list =list(todo.specific_todo_set.all().values_list('content', flat=True)) # 그리고 해당 todo의  수정 이전 sub todo들을 갖고 온다.
            edited_sub_todo_list = form.data.getlist('sub_todos') # 그리고 수정 요청으로 받은 sub todo들을 갖고온다.

            s = set(edited_sub_todo_list)
            todos_to_delete = [x for x in sub_todo_list if x not in s] # 기존의 sub todo들 중에 삭제해야할 리스트
            s = set(sub_todo_list)
            todos_to_add = [x for x in edited_sub_todo_list if x not in s] # 기존의 sub todo에 더하여 주가해야할 리스트

            if len(todos_to_add) == 0 and len(todos_to_delete) == 0: # sub todo가 바뀐 부분이 없다면
                return HttpResponseRedirect('/')  # 그리고 메인페이지로 리다이렉트 해준다.

            for i in todos_to_delete: # 삭제할 sub todo가 있다면
                todo.specific_todo_set.get(content=i).delete() # 해당 sub todo 삭제

            for i in todos_to_add: # 추가할 sub todo가 있다면
                sub_todo = Specific_todo(todo=todo, content=i, is_checked=False)  # 받은 정보를 이용해서 sub todo 객체 생성.
                sub_todo.save() # 그리고 해당 sub todo에 저장해준다.
                if todo.all_done: # 만약 todo가 Done 상태였다면
                    todo.all_done = False # 새로 추가된 sub todo로 인해서 Done에서 빼준다.
                    done = Done.objects.get(todo=todo)
                    done.delete() # 그리고 Done 객체를 삭제해준다.

            all_checked = None
            if len(todos_to_add) == 0: # 만약 추가할 sub todo가 0개일 경우
                all_checked = True
                for i in todo.specific_todo_set.all():
                    if not i.is_checked: # 삭제하고 남은 sub todo들 중에 check되었는지 판별한다.
                        all_checked = False
                        break

            if all_checked: # 그래서 남은 sub todo들이 모두 체크 되었을 경우
                todo.all_done=True # todo의 all_done 플래그를 True로 해주고
                Done(todo=todo, done_date=timezone.now().replace(microsecond=0)).save() # Done 객체를 생성해서 저장합니다.
            todo.save() # 수정된 todo를 저장해준다.
            return HttpResponseRedirect('/') # 그리고 메인페이지로 리다이렉트 해준다.
    else: #만약 request가 POST가 아니었다면
        form = TodoForm() # 빈 form을 넘겨준다.
    return render(request, 'todos/edit_todo.html', {'form': form, 'todo':todo, } ) # 그리고 해당 주소로 form과 todo를 렌더링 해준다.

@login_required # 로그인을 필요로 하는 기능이다.
def delete_todo(request, todo_id):
    try:
        todo = Todo.objects.get(pk=todo_id) # 해당 todo id에 대해 todo 객체를 갖고 온다.
        todo.delete() # 해당 todo를 삭제한다.
    except:
        pass
    return render(request, 'todos/index.html', {'todo_list': User.objects.get(username=request.user.username).todo_set.all()})
    # 해당 유저가 가진 todo리스트들을 해당 주소로 함께 렌더링해준다.


def account_login(request):
    if request.method == 'POST': #만약 POST 방식으로 요청이 넘어왔다면
        form = LoginForm(request.POST) # LoginForm에 대해 넘어온 data저장
        if form.is_valid(): # form이 유효하다면
            username = form['username'].value()
            password = form['password'].value() # 유저네임과 패스워드를 받아온다.
            user = authenticate(request,username=username, password=password) # 그리고 해당 유저에 대해서 인증
            if user is not None: # 만약 해당 유저가 있다면
                login(request, user) # 해당 유저 로그인 해준다.
                return render(request,'todos/index.html', {'todo_list' : User.objects.get(username=request.user.username).todo_set.all()}) # 그리고 메인페이지로 넘겨준다.
            else: # 만약 해당 유저가 없다면
                return render(request, 'todos/login.html') # 로그인 페이지로 넘겨준다.
    return render(request, 'todos/login.html') # 만약 제대로 된 요청이 아니라면 로그인 페이지로 넘겨준다.

@login_required # 로그인을 필요로 하는 기능이다.
def account_logout(request):
    logout(request) # 해당 유저를 로그아웃 시켜준다.
    return render(request, 'todos/login.html') # 그리고 로그인페이지로 넘겨준다.

def account_signup(request):
    if request.method == "POST":
        form = UserForm(request.POST) # UserForm형식에 맞게 넘어온 데이터를 넣어준다.
        if form.is_valid(): # form 이 유효하다면
            new_user = User.objects.create_user(**form.cleaned_data) # 새로운 유저 객체 생성한다.
            login(request, new_user) # 그리고 로그인 해준다.
            return render(request, 'todos/index.html', {'todo_list': User.objects.get(username=request.user.username).todo_set.all()}) # 그 뒤 메인 페이지로 넘겨준다.
        else: # 만약 form이 제대로 되지 않았다면
            return HttpResponse('사용자명과 비밀번호를 다시 입력해주세요. (사용자명 : 4 ~ 20글자, 비밀번호 : 6 ~ 20글자)') # 이러한 문구를 띄워준다.
    else: # 만약 request가 잘못 되었다면
        form = UserForm() # 빈 userform 객체
        return render(request, 'todos/signup.html', {'form': form})  # form과 함께 signup 페이지로 렌더링