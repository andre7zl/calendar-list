from django.urls import path
from django.contrib.auth import views as auth_views
from .views import CreateUser, UserUpdate, UserDetailView

urlpatterns = [
    # path('', view, name='')
    path('login/', auth_views.LoginView.as_view(template_name = 'registration/login.html'), name = "login"),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('user/<int:pk>/', UserDetailView.as_view(), name='user_detail'),
    path('registrar/', CreateUser.as_view(template_name = 'registration/register.html'), name = "register"),
    path('edituser/', UserUpdate.as_view(), name = "edituser"),
]