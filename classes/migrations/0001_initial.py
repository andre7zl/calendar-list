# Generated by Django 5.1.2 on 2024-10-24 12:43

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Turma',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=100)),
                ('serie', models.CharField(choices=[('1', '1º Ano'), ('2', '2º Ano'), ('3', '3º Ano'), ('4', '4º Ano')], max_length=1)),
                ('turno', models.CharField(choices=[('manha', 'Manhã'), ('tarde', 'Tarde'), ('noite', 'Noite')], max_length=5)),
                ('curso', models.CharField(choices=[('edificacoes', 'Edificações'), ('informatica', 'Informática'), ('meio_ambiente', 'Meio Ambiente'), ('matematica', 'Matemática')], max_length=15)),
            ],
        ),
    ]
