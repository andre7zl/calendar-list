from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class CustomUser(AbstractUser):
    id = models.BigAutoField(primary_key=True)

    id_turma = models.PositiveIntegerField(blank=True, null=True)
