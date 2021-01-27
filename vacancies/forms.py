from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django.urls import reverse

from .models import Application


class SignUpForm(UserCreationForm):
    username = forms.CharField(min_length=3, label='Логин')
    first_name = forms.CharField(label='Имя')
    last_name = forms.CharField(label='Фамилия')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'POST'
        self.helper.form_action = reverse('sign_up')
        self.helper.add_input(Submit('submit', 'Зарегистрироваться'))

        self.helper.label_class = 'text-muted'


class ApplicationForm(forms.Form):
    username = forms.CharField(label='Вас зовут')
    phone = forms.CharField(label='Ваш телефон')
    cover_letter = forms.CharField(label='Сопроводительное письмо')

    class Meta:
        model = Application
        fields = ('username', 'phone', 'cover_letter')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'POST'
        self.helper.form_action = reverse('send_application', kwargs={'vacancy_id': 0})
        self.helper.add_input(Submit('submit', 'Отправить отклик'))

        self.helper.form_class = 'card mt-4 mb-3'
        self.helper.label_class = 'mb-1 mt-2'
