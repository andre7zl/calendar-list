# Generated by Django 5.1.2 on 2024-11-26 16:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('classes', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='turma',
            name='nome',
            field=models.CharField(max_length=8, unique=True),
        ),
    ]
