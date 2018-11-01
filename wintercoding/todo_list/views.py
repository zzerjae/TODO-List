from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from . import models, forms
 

def todo_list(request):
    my_todo = models.TODO.objects.filter(author=request.user)
    return render(request, 'todo_list/todo_list.html', {'todos': my_todo})

def todo_add(request):
    if request.method == 'POST':
        form = forms.TODOForm(request.POST)
        if form.is_valid():
            todo = models.TODO()
            todo.title = form.cleaned_data['title']
            todo.content = form.cleaned_data['content']
            if form.cleaned_data['due_by']:
                todo.due_by = form.cleaned_data['due_by']
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


def todo_complete_list(request):
    completed_todo = models.TODO.objects.filter(Q(author=request.user) & Q(status='c'))
    return render(request, 'todo_list/todo_completed_list.html', {'todos': completed_todo})


def todo_reorder(request):
    pass


def todo_detail(request, todo_id):
    pass


def todo_modify(request, todo_id):
    todo = get_object_or_404(models.TODO, pk=todo_id)
    if request.method == 'POST':
        form = forms.TODOModifyForm(request.POST)
        if form.is_valid():
            todo.title = form.cleaned_data['title']
            todo.content = form.cleaned_data['content']
            if form.cleaned_data['due_by']:
                todo.due_by = form.cleaned_data['due_by']
            todo.status = form.cleaned_data['status']
            if todo.status == 'c':
                for t in models.TODO.objects.filter(author=request.user):
                    if t.priority > todo.priority:
                        t.priority -= 1
                        t.save()
                todo.priority = 0
            else:
                old_priority = todo.priority
                new_priority = form.cleaned_data['priority']
                # 우선순위에 변동이 없을 때
                if old_priority == new_priority:
                    if new_priority == 0:
                        todo.priority = models.TODO.objects.filter(author=request.user).last().priority + 1
                # 할 일의 우선순위가 높아졌을때(e.g. 5순위 > 1순위)
                elif old_priority > new_priority:
                    for t in models.TODO.objects.filter(author=request.user):
                        if t.priority < old_priority and t.priority >= new_priority:
                            t.priority += 1
                            todo.priority = new_priority
                            t.save()
                # 할 일의 우선순위가 낮아졌을때(e.g. 1순위 > 5순위)
                else:
                    for t in models.TODO.objects.filter(author=request.user):
                        if t.priority > old_priority and t.priority <= new_priority:
                            t.priority -= 1
                            todo.priority = new_priority
                            t.save()
            todo.save()

            return HttpResponseRedirect('/todo/')
    else:
        form = forms.TODOModifyForm(instance=todo)
    return render(request, 'todo_list/todo_modify.html', {'form': form})



def todo_delete(request, todo_id):
    todo = get_object_or_404(models.TODO, pk=todo_id)
    for t in models.TODO.objects.filter(author=request.user):
        if t.priority > todo.priority:
            t.priority -= 1
            todo.priority = 0
            t.save()
    todo.delete()

    return HttpResponseRedirect('/todo/')


def todo_complete(request, todo_id):
    todo = get_object_or_404(models.TODO, pk=todo_id)
    todo.status = 'c'
    for t in models.TODO.objects.filter(author=request.user):
        if t.priority > todo.priority:
            t.priority -= 1
            t.save()
    todo.priority = 0
    todo.save()

    return HttpResponseRedirect('/todo/')