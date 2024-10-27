from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from classes import models
from django.contrib.auth import get_user_model

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

    