from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, reverse
from django.utils import timezone
from . import models, forms
 

def todo_list(request):
    if request.user.is_authenticated:
        my_todo = models.TODO.objects.filter(author=request.user)
    else:
        my_todo = None
    return render(request, 'todo_list/todo_list.html', {'todos': my_todo})

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

@login_required
def todo_complete_list(request):
    completed_todo = models.TODO.objects.filter(Q(author=request.user) & Q(status='c'))
    return render(request, 'todo_list/todo_completed_list.html', {'todos': completed_todo})

@login_required
def todo_reorder(request, todo_id, priority):
    todo = get_object_or_404(models.TODO, pk=todo_id)
    todos = models.TODO.objects.filter(Q(author=request.user) & Q(status='i'))
    for t in todos:
        if t.priority == todo.priority - 1 and priority == 0:
            t.priority += 1
            todo.priority -= 1
            t.save()
            todo.save()
        elif t.priority == todo.priority + 1 and priority == 1:
            t.priority -= 1
            todo.priority += 1
            t.save()
            todo.save()

    return HttpResponseRedirect('/todo/')

@login_required
def todo_detail(request, todo_id):
    todo = get_object_or_404(models.TODO, pk=todo_id)
    return render(request, 'todo_list/todo_detail.html', {'todo': todo})

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
            todos = models.TODO.objects.filter(Q(author=request.user) & Q(status='i'))
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

@login_required
def todo_delete(request, todo_id):
    todo = get_object_or_404(models.TODO, pk=todo_id)
    for t in models.TODO.objects.filter(Q(author=request.user) & Q(status='i')):
        if t.priority > todo.priority:
            t.priority -= 1
            todo.priority = 0
            t.save()
    todo.delete()

    return HttpResponseRedirect('/todo/')

@login_required
def todo_complete(request, todo_id):
    todo = get_object_or_404(models.TODO, pk=todo_id)
    todo.status = 'c'
    for t in models.TODO.objects.filter(Q(author=request.user) & Q(status='i')):
        if t.priority > todo.priority:
            t.priority -= 1
            t.save()
    todo.priority = 0
    todo.completed_at = timezone.now()
    todo.save()

    return HttpResponseRedirect('/todo/')