from django.views.generic.edit import CreateView
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from .forms import UsuarioForm

# Create your views here.
class CreateUser(CreateView):
    template_name = "register/register.html"  # Ajuste o caminho se necessário
    form_class = UsuarioForm
    success_url = reverse_lazy('login')  # Substitua pelo nome correto da URL

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['titulo'] = "Registro de novo usuário"
        context['botão'] = "Cadastrar"
        return context