from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .forms import TaskForm
from django.contrib import messages
from django.http import JsonResponse
from .models import Task
from datetime import datetime, date, timedelta
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.views import View
from braces.views import LoginRequiredMixin, GroupRequiredMixin
from django.views.generic import TemplateView
from django.utils import timezone
from classes.models import Turma

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


class CalendarView(TemplateView):
    template_name = 'tasks/calendar.html'

    def get_context_data(self, **kwargs):
        user_turma = getattr(self.request.user, 'turma', None)
        context = super().get_context_data(**kwargs)
        is_discente = self.request.user.groups.filter(name='Discente').exists()
        is_docente = self.request.user.groups.filter(name='Docente').exists()
        today = timezone.localdate()

        if is_discente and user_turma:
            events_today = Task.objects.filter(
                turma=user_turma,
                start_date__lte=today,
                end_date__gte=today
            )

        elif is_docente:
            events_today = Task.objects.filter(
                usuario=self.request.user,
                start_date__lte=today,
                end_date__gte=today
            )

        else:
            events_today = Task.objects.filter(
                start_date__lte=today,
                end_date__gte=today
            )

        context['events_today'] = events_today
        context['turmas'] = Turma.objects.all()
        return context

def home(request):
    return render(request, 'tasks/home.html')



class TaskEventsView(View):
    def get(self, request, *args, **kwargs):
        turma_id = request.GET.get('turma_id', None)
        user_turma = request.user.turma
        is_discente = request.user.groups.filter(name='Discente').exists()
        is_docente = self.request.user.groups.filter(name='Docente').exists()
        
        if turma_id:
            tasks = Task.objects.filter(turma_id=turma_id)
        elif is_discente and user_turma:
            tasks = Task.objects.filter(turma=user_turma)
        elif is_docente:
            tasks = Task.objects.filter(usuario=self.request.user)
        else:
            tasks = Task.objects.all()

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
    

class EventCountView(LoginRequiredMixin,TemplateView):
    login_url = reverse_lazy('login')
    template_name = 'tasks/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        today = timezone.localdate()
        start_of_week = today
        end_of_week = today + timedelta(days=(6 - today.weekday()))

        is_discente = user.groups.filter(name='Discente').exists()
        is_docente = self.request.user.groups.filter(name='Docente').exists()

        if is_discente:
            tasks_today = Task.objects.filter(turma=self.request.user.turma, start_date__lte=today, end_date__gte=today)
            tasks_week = Task.objects.filter(turma=self.request.user.turma, start_date__gte=today, end_date__lte=end_of_week)
            total_tasks = Task.objects.filter(turma=self.request.user.turma, start_date__gte=today)
            context['tasks'] = Task.objects.filter(turma=self.request.user.turma)
            
        if is_docente:
            tasks_today = Task.objects.filter(usuario=self.request.user, start_date__lte=today, end_date__gte=today)
            tasks_week = Task.objects.filter(usuario=self.request.user, start_date__gte=today, end_date__lte=end_of_week)
            total_tasks = Task.objects.filter(usuario=self.request.user, start_date__gte=today)
            context['tasks'] = Task.objects.filter(usuario=self.request.user)

        context['tasks_today_count'] = tasks_today.count()
        context['tasks_week_count'] = tasks_week.count()
        context['total_tasks_count'] = total_tasks.count()

        return context
    
from django.http import JsonResponse
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Task

class MonthlyDataView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        monthly_data = [0] * 12
        user = request.user
        is_discente = user.groups.filter(name='Discente').exists()
        is_docente = user.groups.filter(name='Docente').exists()
        # Filtra as tarefas da turma do usuário, se ele for Discente
        if is_discente and hasattr(user, 'turma'):
            tasks = Task.objects.filter(turma=user.turma)
        elif is_docente:
            tasks = Task.objects.filter(usuario=self.request.user)
        else:
            tasks = Task.objects.all()

        for task in tasks:
            if task.start_date:
                month = task.start_date.month - 1
                monthly_data[month] += 1

        return JsonResponse(monthly_data, safe=False)
    

class WeeklyDataView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        month = int(request.GET.get('month', date.today().month))  # Obter o mês do parâmetro ou o mês atual
        year = int(request.GET.get('year', date.today().year))  # Obter o ano do parâmetro ou o ano atual
        
        # Inicializar a lista de semanas
        weekly_data = [0, 0, 0, 0]

        # Verificar se o usuário é Discente
        user = request.user
        is_discente = user.groups.filter(name='Discente').exists()
        is_docente = user.groups.filter(name='Docente').exists()

        if is_discente:
            tasks = Task.objects.filter(turma=user.turma)
        if is_docente:
            tasks = Task.objects.filter(usuario=self.request.user)

        month_tasks = tasks.filter(start_date__year=year, start_date__month=month)

        # Contar eventos por semana
        for task in month_tasks:
            week_number = (task.start_date.day - 1) // 7  # Obter a semana do mês (0 a 3)
            weekly_data[week_number] += 1

        return JsonResponse(weekly_data, safe=False)

class TasksByTurmaView(LoginRequiredMixin, ListView):
    model = Task
    template_name = 'tasks/turma_tasks.html'
    context_object_name = 'tasks'

    def get_queryset(self):
        user = self.request.user
        user_turma = getattr(user, 'turma', None)
        # Verifica se o usuário é "Discente" e tem uma turma associada
        if user.groups.filter(name='Discente').exists() and user_turma:
            return Task.objects.filter(turma=user_turma)
        else:
            # Se não for "Discente", exibe todas as tarefas
            return Task.objects.all()
