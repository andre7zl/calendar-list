# Generated by Django 5.1.2 on 2024-12-01 18:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0003_alter_task_usuario'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='task',
            name='subs',
        ),
        migrations.RemoveField(
            model_name='task',
            name='total_subs',
        ),
    ]