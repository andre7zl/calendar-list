from django.db import models
from django.contrib.auth.models import Group
from django.core.exceptions import ValidationError

class Turma(models.Model):
    TURNO_CHOICES = [
        ('manha', 'Manhã'),
        ('tarde', 'Tarde'),
        ('noite', 'Noite'),
    ]

    CURSO_CHOICES = [
        ('edificacoes', 'Edificações'),
        ('informatica', 'Informática'),
        ('meio_ambiente', 'Meio Ambiente'),
        ('matematica', 'Matemática'),
    ]

    SERIE_CHOICES = [
        ('1', '1º Ano'),
        ('2', '2º Ano'),
        ('3', '3º Ano'),
        ('4', '4º Ano'),
    ]

    nome = models.CharField(max_length=8, unique=True)
    serie = models.CharField(max_length=1, choices=SERIE_CHOICES)
    turno = models.CharField(max_length=5, choices=TURNO_CHOICES)
    curso = models.CharField(max_length=15, choices=CURSO_CHOICES)

    def __str__(self):
        return f"{self.nome} - {self.serie}º {self.turno} ({self.curso})"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        group_name = f"{self.nome}_{self.serie}_{self.turno}_{self.curso}"
        Group.objects.get_or_create(name=group_name)

    def can_delete(self):
        if self.customuser_set.exists():
            return "Não é possível excluir a turma porque existem usuários associados a ela, verifique com os usuários e tente novamente"
        if self.task_set.exists():
            return "Não é possível excluir a turma porque existem eventos associadas a ela, verifique os eventos e tente novamente"
        return None


    def delete(self, *args, **kwargs):
        error_message = self.can_delete()
        if error_message:
            raise ValidationError(error_message)
        super().delete(*args, **kwargs)

