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
    if request.user.is_authenticated:
        user = User.objects.get(username = request.user.username)
        todo_list = user.todo_set.all()
        return render(request, 'todos/index.html', {'todo_list': todo_list })
    else:
        return render(request, 'todos/login.html')
class DetailView(generic.DetailView):
    model = Todo
    template_name = 'todos/detail.html'

@login_required
def check_todo(request, todo_id):
    todo = get_object_or_404(Todo, pk=todo_id)
    checked_list = []
    checked_list.extend(request.POST.getlist('sub_todo'))
    all_sub_todos = todo.specific_todo_set.values('id')
    for i in range(len(all_sub_todos)):
        checked_todo = todo.specific_todo_set.get(pk=all_sub_todos[i]['id'])
        if str(checked_todo.id) in checked_list:
            checked_todo.is_checked = True
        else:
            checked_todo.is_checked = False
        checked_todo.save()
    return HttpResponseRedirect(reverse('todos:done', args=(todo.id, )))

@login_required
def done(request, todo_id):
    all_done = True
    todo = get_object_or_404(Todo, pk=todo_id)
    for i in todo.specific_todo_set.all():
        if i.is_checked == False:
            all_done = False
            todo.all_done = False
            todo.save()
            try:
                d = Done.objects.get(todo=todo)
                d.delete()
                todo.done_date = None
                todo.save()
            except Done.DoesNotExist:
                pass
            break
    if all_done:
        todo.all_done = True
        d = Done(todo=todo, done_date=timezone.now().replace(microsecond=0))
        d.save()
        todo.save()
    return render(request, 'todos/index.html', {'todo_list': User.objects.get(username=request.user.username).todo_set.all()})

@login_required
def write_todo(request):
    if request.method == 'POST':
        form = TodoForm(request.POST)
        print(form.errors)
        if form.is_valid():
            print("It is valid!")
            todo = Todo(user=request.user, pub_date=timezone.now().replace(microsecond=0), due_date=form['due_date'].value(), title = form['title'].value(), priority = form['priority'].value(), all_done=False)
            todo.save()
            for i in form.data.getlist('sub_todos'):
                sub_todo = Specific_todo(todo=todo, content=i, is_checked=False)
                sub_todo.save()
            return HttpResponseRedirect('/todos/')
    else:
        form = TodoForm()
    return render(request, 'todos/write_todo.html', {'form': form,} )


@login_required
def edit_todo(request, todo_id):
    todo = Todo.objects.get(pk=todo_id)
    if request.method == 'POST':
        form = TodoForm(request.POST)
        if form.is_valid():
            todo.due_date =form['due_date'].value()
            todo.title = form['title'].value()
            todo.priority = form['priority'].value()
            todo.save()

            sub_todo_list = todo.specific_todo_set.all().values_list('content', flat=True)
            edited_sub_todo_list = form.data.getlist('sub_todos')

            for i in sub_todo_list:
                if i not in edited_sub_todo_list:
                    print('1')
                    Specific_todo.objects.get(content=i).delete()

            for i in edited_sub_todo_list:
                try :
                    Specific_todo.objects.get(content=i)
                except ObjectDoesNotExist:
                    print('yes')
                    sub_todo = Specific_todo(todo=todo, content=i, is_checked=False)
                    sub_todo.save()
            return HttpResponseRedirect('/todos/')
    else:
        form = TodoForm()
    return render(request, 'todos/edit_todo.html', {'form': form, 'todo':todo,} )

@login_required
def delete_todo(request, todo_id):
    todo = Todo.objects.get(pk=todo_id)
    todo.delete()
    return render(request, 'todos/index.html', {'todo_list': User.objects.get(username=request.user.username).todo_set.all()})


def account_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form['username'].value()
            password = form['password'].value()
            user = authenticate(request,username=username, password=password)
            if user is not None:
                login(request, user)
                # return render(request, 'todos/index.html', {'todo_list': Todo.objects.all()})
                return render(request,'todos/index.html', {'todo_list' : User.objects.get(username=request.user.username).todo_set.all()})
            else:
                return render(request, 'todos/login.html')
    return render(request, 'todos/login.html')

@login_required
def account_logout(request):
    logout(request)
    return render(request, 'todos/login.html')

def account_signup(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            new_user = User.objects.create_user(**form.cleaned_data)
            login(request, new_user)
            return render(request, 'todos/index.html', {'todo_list': User.objects.get(username=request.user.username).todo_set.all()})
        else:
            return HttpResponse('사용자명과 비밀번호를 다시 입력해주세요. (사용자명 : 4 ~ 20글자, 비밀번호 : 6 ~ 20글자)')
    else:
        form = UserForm()
        return render(request, 'todos/signup.html', {'form': form})