# Generated by Django 5.1.2 on 2024-10-26 19:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0003_remove_task_turma_delete_turma'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='id_turma',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
    ]
