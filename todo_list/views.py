import datetime

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, reverse
from django.utils import timezone

from . import models, forms

# 마감기한 체크하는 함수
# 편의상 날짜를 등록 안하면 오늘로
# 시간을 등록 안하면 11시 59분으로 두고 계산한다.
def check_deadline(func):
    def wrapper(*args, **kwargs):
        r = func(*args, **kwargs)
        request = args[0]

        now = datetime.datetime.now()
        
        if not request.user.is_authenticated:
            return r

        for todo in models.TODO.objects.filter(Q(author=request.user) & Q(status='i')|Q(status='e')):
            if todo.due_date or todo.due_time:
                date = datetime.datetime(
                    todo.due_date.year,
                    todo.due_date.month,
                    todo.due_date.day,
                ) if todo.due_date else datetime.datetime.now()
                if todo.due_time:
                    date = date.replace(
                        hour=todo.due_time.hour,
                        minute=todo.due_time.minute,
                        second=todo.due_time.second
                    )
                else:
                    date = date.replace(
                        hour=23,
                        minute=59,
                        second=00
                    )
                # 마감기한을 초과한 상황
                if now > date + datetime.timedelta(seconds=60):
                    time = now - date
                    day = int(time.total_seconds() // (60*60*24))
                    time -= datetime.timedelta(seconds=day * 60 * 60 * 24)
                    hour = int(time.total_seconds() // (60 * 60))
                    time -= datetime.timedelta(seconds=hour * 60 * 60)
                    minute = int(time.total_seconds() // (60))
    
                    todo.status = 'e'
                    todo.save()
                    warning_text = '{0}: {1}가 마감 기한을 {2}일 {3}시 {4}분 초과했습니다.'.format(
                        todo.priority,
                        todo.title,
                        day,
                        hour,
                        minute
                    )
                    messages.error(request, warning_text)

        return r
    return wrapper

@check_deadline
def todo_list(request):
    if request.user.is_authenticated:
        my_todo = models.TODO.objects.filter(author=request.user)
    else:
        my_todo = None
    return render(request, 'todo_list/todo_list.html', {'todos': my_todo})

@check_deadline
@login_required
def todo_add(request):
    if request.method == 'POST':
        form = forms.TODOForm(request.POST)
        if form.is_valid():
            todo = models.TODO()
            todo.title = form.cleaned_data['title']
            todo.content = form.cleaned_data['content']
            if form.cleaned_data['due_date']:
                todo.due_date = form.cleaned_data['due_date']
            if form.cleaned_data['due_time']:
                todo.due_time = form.cleaned_data['due_time']
            todo.author = request.user
            todos = models.TODO.objects.filter(author=request.user)
            if todos:
                todo.priority = todos.last().priority + 1
            else:
                todo.priority = 1
            todo.save()

            return HttpResponseRedirect('/todo/')

    else:
        form = forms.TODOForm()

    return render(request, 'todo_list/todo_add.html', {'form': form})

@check_deadline
@login_required
def todo_complete_list(request):
    completed_todo = models.TODO.objects.filter(Q(author=request.user) & Q(status='c'))
    return render(request, 'todo_list/todo_completed_list.html', {'todos': completed_todo})

@check_deadline
@login_required
def todo_reorder(request, todo_id, priority):
    todo = get_object_or_404(models.TODO, pk=todo_id)
    todos = models.TODO.objects.filter(Q(author=request.user) & Q(status='i')|Q(status='e'))
    for t in todos:
        if t.priority == todo.priority - 1 and priority == 0:
            t.priority += 1
            todo.priority -= 1
            t.save()
            todo.save()
            break
        elif t.priority == todo.priority + 1 and priority == 1:
            t.priority -= 1
            todo.priority += 1
            t.save()
            todo.save()
            break

    return HttpResponseRedirect('/todo/')

@check_deadline
@login_required
def todo_detail(request, todo_id):
    todo = get_object_or_404(models.TODO, pk=todo_id)
    return render(request, 'todo_list/todo_detail.html', {'todo': todo})

@check_deadline
@login_required
def todo_modify(request, todo_id):
    todo = get_object_or_404(models.TODO, pk=todo_id)
    if request.method == 'POST':
        form = forms.TODOModifyForm(request.POST)
        if form.is_valid():
            todo.title = form.cleaned_data['title']
            todo.content = form.cleaned_data['content']
            if form.cleaned_data['due_date']:
                todo.due_date = form.cleaned_data['due_date']
            if form.cleaned_data['due_time']:
                todo.due_time = form.cleaned_data['due_time']
            todo.status = form.cleaned_data['status']
            todos = models.TODO.objects.filter(Q(author=request.user) & Q(status='i')|Q(status='e'))
            if todo.status == 'c':
                for t in todos:
                    if t.priority > todo.priority:
                        t.priority -= 1
                        t.save()
                todo.priority = 0
                todo.completed_at = timezone.now()
            else:
                old_priority = todo.priority
                new_priority = form.cleaned_data['priority']
                # 우선순위에 변동이 없을 때
                if old_priority == new_priority:
                    if new_priority == 0:
                        if todos:
                            todo.priority = todos.last().priority + 1
                        else:
                           todo.priority = 1
                # 할 일의 우선순위가 높아졌을때(e.g. 5순위 > 1순위)
                elif old_priority > new_priority:
                    for t in todos:
                        if t.priority < old_priority and t.priority >= new_priority:
                            t.priority += 1
                            todo.priority = new_priority
                            t.save()
                # 할 일의 우선순위가 낮아졌을때(e.g. 1순위 > 5순위)
                else:
                    for t in todos:
                        if t.priority > old_priority and t.priority <= new_priority:
                            t.priority -= 1
                            todo.priority = new_priority
                            t.save()
            todo.save()

            return HttpResponseRedirect(reverse('todo_list:todo_detail', kwargs={'todo_id': todo.id}))
    else:
        form = forms.TODOModifyForm(instance=todo)
    return render(request, 'todo_list/todo_modify.html', {'form': form})

@check_deadline
@login_required
def todo_delete(request, todo_id):
    todo = get_object_or_404(models.TODO, pk=todo_id)
    for t in models.TODO.objects.filter(Q(author=request.user) & Q(status='i')|Q(status='e')):
        if t.priority > todo.priority:
            t.priority -= 1
            todo.priority = 0
            t.save()
    todo.delete()

    return HttpResponseRedirect('/todo/')

@check_deadline
@login_required
def todo_complete(request, todo_id):
    todo = get_object_or_404(models.TODO, pk=todo_id)
    todo.status = 'c'
    for t in models.TODO.objects.filter(Q(author=request.user) & Q(status='i')|Q(status='e')):
        if t.priority > todo.priority:
            t.priority -= 1
            t.save()
    todo.priority = 0
    todo.completed_at = timezone.now()
    todo.save()

    return HttpResponseRedirect('/todo/')