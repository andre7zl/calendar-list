from django.views.generic.edit import CreateView
from django.contrib.auth.models import User, Group
from django.urls import reverse_lazy
from .forms import UsuarioForm
from django.shortcuts import get_object_or_404


class CreateUser(CreateView):
    template_name = "register/register.html"
    form_class = UsuarioForm
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        grupo = get_object_or_404(Group, name="Discente")
        url = super().form_valid(form)
        self.object.groups.add(grupo)
        self.object.save()
        return url

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['titulo'] = "Registro de novo usuário"
        context['botão'] = "Cadastrar"
        return context