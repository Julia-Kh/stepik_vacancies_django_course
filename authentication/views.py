from django.contrib.auth.views import LoginView
from django.views.generic import CreateView

from .forms import SignUpForm


class SignupView(CreateView):
    form_class = SignUpForm
    success_url = '/login'
    template_name = 'authentication/sign_up.html'


class LogInView(LoginView):
    redirect_authenticated_user = True
    template_name = 'authentication/login.html'
