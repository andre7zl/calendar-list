from django.urls import path
from .views import TurmaCreateView

urlpatterns = [
    # path('', view, name='')
    path('cadastrar-turma/', TurmaCreateView.as_view(template_name = 'classes/cadastrar_turma.html'), name='cadastrar_turma'),
]