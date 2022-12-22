from django.urls import reverse_lazy
from django.views import generic
from .forms import CustomUserCreationForm
from .models import CustomUser

class SignUpPageView(generic.CreateView):
    form_class = CustomUserCreationForm
    model = CustomUser
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"
