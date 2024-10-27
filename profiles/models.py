from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class CustomUser(AbstractUser):
    id = models.BigAutoField(primary_key=True)

    turma = models.ForeignKey('classes.Turma', on_delete=models.SET_NULL, blank=True, null=True)
