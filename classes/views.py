from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from .models import Turma
from .forms import TurmaForm
from django.contrib.auth.models import Group


class TurmaCreateView(CreateView):
    model = Turma
    form_class = TurmaForm
    template_name = 'classes/cadastrar_turma.html'
    success_url = reverse_lazy('task-list')

    def form_valid(self, form):
        response = super().form_valid(form)
        
        turma = form.instance
        group_name = f"{turma.nome}_{turma.serie}_{turma.turno}_{turma.curso}"
        Group.objects.get_or_create(name=group_name)
        
        return response


