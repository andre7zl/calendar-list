from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from classes import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

User = get_user_model()

class UsuarioForm(UserCreationForm):
    email = forms.EmailField(max_length=100)
    turma = forms.ModelChoiceField(queryset=models.Turma.objects.all(), required=True)
    class Meta:
        model = User
        fields = ['username', 'email', 'turma', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.id_turma = self.cleaned_data['turma'].id  
        if commit:
            user.save()
        return user

    
    def form_valid(self, form):
        user = form.instance
        old_turma = user.turma
        new_turma = form.cleaned_data['turma'] 

        if old_turma != new_turma:
            if old_turma and Group.objects.filter(name=old_turma.name).exists():
                old_group = Group.objects.get(name=old_turma.name)
                user.groups.remove(old_group)

            if new_turma and Group.objects.filter(name=new_turma.name).exists():
                new_group = Group.objects.get(name=new_turma.name)
                user.groups.add(new_group)

        return super().form_valid(form)