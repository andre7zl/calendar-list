from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .forms import TaskForm
from django.contrib import messages
from django.http import JsonResponse
from .models import Task
from datetime import datetime, timedelta
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.views import View
from braces.views import LoginRequiredMixin, GroupRequiredMixin



class TaskListView(GroupRequiredMixin, LoginRequiredMixin, ListView):
    group_required = u"Docente"
    login_url = reverse_lazy('login')
    model = Task
    template_name = 'tasks/list.html'
    context_object_name = 'tasks'
    ordering = '-created_at'

    def get_queryset(self):
        self.tasks = Task.objects.filter(usuario=self.request.user)
        return self.tasks

class TaskDetailView(DetailView):
    model = Task
    template_name = 'tasks/task.html'
    context_object_name = 'task'


class TaskCreateView(GroupRequiredMixin, LoginRequiredMixin, CreateView):
    group_required = u"Docente"
    login_url = reverse_lazy('login')
    model = Task
    form_class = TaskForm
    template_name = 'tasks/addtask.html'
    success_url = reverse_lazy('task-list')

    def form_valid(self, form):

        form.instance.usuario = self.request.user

        url =  super().form_valid(form)


        return url


class TaskUpdateView(GroupRequiredMixin, LoginRequiredMixin, UpdateView):
    group_required = u"Docente"
    login_url = reverse_lazy('login')
    model = Task
    form_class = TaskForm
    template_name = 'tasks/edittask.html'
    context_object_name = 'task'
    success_url = reverse_lazy('task-list')

    def form_valid(self, form):
        return super().form_valid(form)


class TaskDeleteView(GroupRequiredMixin, LoginRequiredMixin,  DeleteView):
    group_required = u"Docente"
    login_url = reverse_lazy('login')
    model = Task
    template_name = 'tasks/deletetask.html'  # crie um template para confirmar a exclusão
    success_url = reverse_lazy('task-list')

    def delete(self, request, *args, **kwargs):
        messages.info(request, 'Tarefa deletada com sucesso.')
        return super().delete(request, *args, **kwargs)




def calendar(request):
    return render(request, 'tasks/calendar.html')


def home(request):
    return render(request, 'tasks/home.html')



class TaskEventsView(View):
    def get(self, request, *args, **kwargs):

        user_turma = request.user.turma

        is_discente = request.user.groups.filter(name='Discente').exists()

        if is_discente:
            # Se for um discente, filtra as tarefas de todos os usuários do grupo
            tasks = Task.objects.filter(turma=user_turma)
        else:
            # Se não for um discente, filtra apenas as tarefas criadas pelo usuário
            tasks = Task.objects.filter(usuario=request.user)

        events = []

        for task in tasks:
            if task.start_date and task.start_time and task.end_date and task.end_time:
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
