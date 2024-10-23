from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .forms import TaskForm
from django.contrib import messages
from django.http import JsonResponse
from .models import Task
from .models import Task
from datetime import datetime, timedelta

def taskList(request):
    tasks = Task.objects.all().order_by('-created_at')
    return render(request, 'tasks/list.html', {'tasks':tasks})

def taskView(request, id):
    task = get_object_or_404(Task, pk=id)
    return render(request, 'tasks/task.html', {'task': task})

def newTask(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        
        if form.is_valid():
            task = form.save(commit=False)
            task.done = 'doing'
            task.save()
            return redirect('task-list') 
    else:
        form = TaskForm()
    
    return render(request, 'tasks/addtask.html', {'form': form})


def editTask(request, id):
    task = get_object_or_404(Task, pk=id)
    form = TaskForm(instance=task)

    if(request.method == 'POST'):
        form = TaskForm(request.POST, instance=task)

        if(form.is_valid()):
            task.save()
            return redirect('task-list')
        else:
            return render(request, 'task/edittask.html', {'form': form, 'task': task})
    else:
        return render(request, 'tasks/edittask.html', {'form': form, 'task': task})

def deleteTask(request, id):
    task = get_object_or_404(Task, pk=id)
    task.delete()

    messages.info(request, 'Tarefa deletada com sucesso.')

    return redirect('task-list')


def helloWorld(request):
    return HttpResponse('Hello World!')

def calendar(request):
    return render(request, 'tasks/calendar.html')

def home(request):
    return render(request, 'tasks/home.html')

def yourName(request, name):
    return render(request, 'tasks/yourname.html', {'name':name})

def task_events(request):
    tasks = Task.objects.all()
    events = []

def task_events(request):
    tasks = Task.objects.all()
    events = []

    for task in tasks:
        start_datetime = datetime.combine(task.start_date, task.start_time)
        end_datetime = datetime.combine(task.end_date, task.end_time)
        events.append({
            'id': task.id,
            'title': task.title,
            'start': start_datetime.isoformat(),
            'end': end_datetime.isoformat(),
            'description': task.description,
        })

    return JsonResponse(events, safe=False)

