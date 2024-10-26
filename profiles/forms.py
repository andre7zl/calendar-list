from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from classes import models

class UsuarioForm(UserCreationForm):
    email = forms.EmailField(max_length=100)
    turma = forms.ModelChoiceField(queryset=models.Turma.objects.all(), required=True)
    class Meta:
        model = User
        fields = ['username', 'email', 'turma', 'password1', 'password2']

    