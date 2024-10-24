from django.views.generic.edit import CreateView
from django.contrib.auth.models import User

# Create your views here.
class CreateUser(CreateView):
    template_name = "register/html"
    model = User
    fields = ['username', 'email', 'password']