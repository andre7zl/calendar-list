from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from .models import Turma
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .forms import TurmaForm
from django.contrib.auth.models import Group
from django.urls import reverse_lazy
from django.views.generic import DeleteView
from .models import Turma

class TurmaCreateView(CreateView):
    model = Turma
    form_class = TurmaForm
    template_name = 'classes/cadastrar_turma.html'
    success_url = reverse_lazy('lista-turmas')

    def form_valid(self, form):
        response = super().form_valid(form)
        
        turma = form.instance
        group_name = f"{turma.nome}_{turma.serie}_{turma.turno}_{turma.curso}"
        Group.objects.get_or_create(name=group_name)
        
        return response

class ListaTurmas(ListView):
    model = Turma
    template_name = 'classes/lista_turmas.html'
    context_object_name = 'turmas'

class TurmaDeleteView(DeleteView):
    model = Turma
    template_name = 'classes/deletar_turma.html'  
    success_url = reverse_lazy('lista-turmas')

    def post(self, request, *args, **kwargs):
        turma = self.get_object()
        group_name = f"{turma.nome}_{turma.serie}_{turma.turno}_{turma.curso}"
        
        group = Group.objects.filter(name=group_name).first()  
        if group:
            group.delete() 

        return super().delete(request, *args, **kwargs)
