from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit


class SignUpForm(UserCreationForm):
    login = forms.CharField(min_length=3)
    first_name = forms.CharField()
    last_name = forms.CharField()
    password = forms.PasswordInput()
    class Meta:
        model = User
        fields = ('login', 'first_name', 'last_name', 'password')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
