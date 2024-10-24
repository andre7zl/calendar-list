from django.urls import path
from .views import TurmaCreateView, TurmaDeleteView
from .views import ListaTurmas

urlpatterns = [
    # path('', view, name='')
    path('cadastrar-turma/', TurmaCreateView.as_view(template_name = 'classes/cadastrar_turma.html'), name='cadastrar_turma'),
    path('turmas/', ListaTurmas.as_view(), name='lista-turmas'),
    path('turmas/deletar/<int:pk>/', TurmaDeleteView.as_view(), name='delete-turma'),
]