from django.urls import path
from . import views
from .views import TaskListView, TaskDetailView, TaskCreateView, TaskUpdateView, TaskDeleteView, TaskEventsView, CalendarView, EventCountView, MonthlyDataView, WeeklyDataView

urlpatterns = [
    path('dashboard/', EventCountView.as_view(), name='dashboard'),
    path('weekly-data/', WeeklyDataView.as_view(), name='weekly-data'),
    path('', CalendarView.as_view(), name='calendar'),
    path('list/', TaskListView.as_view(), name='task-list'),
    path('monthly-data/', MonthlyDataView.as_view(), name='monthly-data'),
    path('task/<int:pk>/', TaskDetailView.as_view(), name='task-view'),  # Use pk para ID
    path('newtask/', TaskCreateView.as_view(), name='new-task'),
    path('list/edit/<int:pk>/', TaskUpdateView.as_view(), name='edit-task'),  # Use pk para ID
    path('list/delete/<int:pk>/', TaskDeleteView.as_view(), name='delete-task'),  # Use pk para ID
    path('api/tasks/', TaskEventsView.as_view(), name='task_events'),  # Adiciona a nova view
]
