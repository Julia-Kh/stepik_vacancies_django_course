from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.urls import reverse

from .models import Application
from .models import Company
from .models import Vacancy


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
        self.helper.form_action = reverse('vacancy', kwargs={'vacancy_id': 0})
        self.helper.add_input(Submit('submit', 'Отправить отклик'))

        self.helper.form_class = 'card mt-4 mb-3'
        self.helper.label_class = 'mb-1 mt-2'


class CompanyForm(forms.ModelForm):

    class Meta:
        model = Company
        fields = ('title', 'location', 'description', 'employee_count')
        labels = {
            'title': 'Название компании',
            'location': 'География',
            'description': 'Информация о компании',
            'employee_count': 'Количество человек в компании',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'POST'
        self.helper.add_input(Submit('submit', 'Сохранить'))


class VacancyForm(forms.ModelForm):

    class Meta:
        model = Vacancy
        fields = ('title', 'specialty', 'skills', 'description', 'salary_from', 'salary_to')
        labels = {'title': 'Название вакансии',
                  'specialty': 'Специализация',
                  'skills': 'Требуемые навыки',
                  'description': 'Описание вакансии',
                  'salary_from': 'Зарплата от',
                  'salary_to': 'Зарплата до',
                  }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'POST'
        self.helper.add_input(Submit('submit', 'Сохранить'))
