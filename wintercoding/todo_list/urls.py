from django.urls import path
from . import views


app_name = 'todo_list'
urlpatterns = [
    path('', views.todo_list, name='todo_list'),
    path('add/', views.todo_add, name='todo_add'),
    path('complete/', views.todo_complete_list, name='todo_complete_list'),
    path('reorder/', views.todo_reorder, name='todo_reorder'),
    path('<int:todo_id>/', views.todo_detail, name='todo_detail'),
    path('<int:todo_id>/modify/', views.todo_modify, name='todo_modify'),
    path('<int:todo_id>/delete/', views.todo_delete, name='todo_delete'),
    path('<int:todo_id>/complete/', views.todo_complete, name='todo_complete'),
]