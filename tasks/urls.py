from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('calendar/', views.calendar, name='calendar'),
    path('helloworld/', views.helloWorld),
    path('list/', views.taskList, name='task-list'),
    path('task/<int:id>', views.taskView, name="task-view"),
    path('newtask/', views.newTask, name="new-task"),
    path('list/edit/<int:id>', views.editTask, name="edit-task"),
    path('list/delete/<int:id>', views.deleteTask, name="delete-task"),
    path('yourname/<str:name>', views.yourName, name='your-name'),
    path('api/tasks/', views.task_events, name='task_events'),
]