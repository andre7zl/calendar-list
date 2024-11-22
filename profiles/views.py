from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.models import User, Group
from django.views.generic.detail import DetailView
from .models import CustomUser
from django.urls import reverse_lazy
from .forms import UsuarioForm
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.contrib import messages
from braces.views import LoginRequiredMixin, GroupRequiredMixin

class CreateUser(CreateView):
    template_name = "register/register.html"
    form_class = UsuarioForm
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        turma = form.cleaned_data['turma']
        group_name = f"{turma.nome}_{turma.serie}_{turma.turno}_{turma.curso}"
        group_turma = get_object_or_404(Group, name=group_name)
        grupo = get_object_or_404(Group, name="Discente")
        url = super().form_valid(form)
        self.object.groups.add(group_turma)
        self.object.groups.add(grupo)
        self.object.save()
        return url

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['titulo'] = "Registro de novo usuário"
        context['botão'] = "Cadastrar"
        return context

class UserUpdate(UpdateView):
    template_name = "registration/edituser.html"
    model = CustomUser
    fields = ['username', 'email', 'turma']
    success_url = reverse_lazy("dashboard")

    def get_object(self, queryset=None):
        self.object = self.request.user
        return self.object

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        user = self.request.user
    
        if user.groups.filter(name='Docente').exists():
            form.fields.pop('turma')
        elif user.groups.filter(name='Discente').exists():
            pass
        
        return form

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        return context

    def form_valid(self, form):
        user = form.instance

        original_user = CustomUser.objects.get(pk=user.pk)
        old_turma = original_user.turma
        new_turma = form.cleaned_data['turma']

        print(f"Old turma: {old_turma}")
        print(f"New turma: {new_turma}")

        if old_turma != new_turma:
            old_group_name = f"{old_turma.nome}_{old_turma.serie}_{old_turma.turno}_{old_turma.curso}"
            old_group = Group.objects.filter(name=old_group_name).first()
            if old_group:
                print(f"Removing from group: {old_group.name}")
                user.groups.remove(old_group)
                
            user.turma = new_turma

            new_group_name = f"{new_turma.nome}_{new_turma.serie}_{new_turma.turno}_{new_turma.curso}"
            new_group, created = Group.objects.get_or_create(name=new_group_name)
            print(f"Adding to group: {new_group.name}")
            user.groups.add(new_group)

        user.save()
        return super().form_valid(form)


class UserDetailView(GroupRequiredMixin, DetailView):
    group_required = u"Docente"
    login_url = reverse_lazy('login')
    model = CustomUser
    template_name = "registration/user_detail.html"
    context_object_name = "user_detail"

    def post(self, request, *args, **kwargs):
        user = self.get_object()  # Obtém o usuário a partir da URL
        tutor_group, _ = Group.objects.get_or_create(name="Tutor")

        if "toggle_tutor" in request.POST:
            if user.groups.filter(name="Tutor").exists():
                user.groups.remove(tutor_group)
                messages.success(request, f"{user.username} não é mais Tutor.")
            else:
                user.groups.add(tutor_group)
                messages.success(request, f"{user.username} agora é Tutor.")

        return redirect('user_detail', pk=user.id)

