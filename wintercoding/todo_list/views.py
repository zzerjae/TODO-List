from django.shortcuts import render
from . import models
 

def todo_list(request):
    my_todo = models.TODO.objects.filter(author=request.user)
    return render(request, 'todo_list/todo_list.html', {'todos': my_todo})

def todo_add(request):
    pass


def todo_complete_list(request):
    pass


def todo_reorder(request):
    pass


def todo_detail(request, id):
    pass


def todo_modify(request):
    pass


def todo_delete(request):
    pass


def todo_complete(request):
    pass