from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView
from django.db.models import Count
from django.http import HttpResponseNotFound
from django.http import HttpResponseServerError
from django.shortcuts import get_object_or_404
from django.views.generic import CreateView
from django.views.generic import TemplateView

from .models import Company
from .models import Specialty
from .models import Vacancy


class MainListView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super(MainListView, self).get_context_data(**kwargs)
        context['specialties'] = Specialty.objects.annotate(num_vacancies=Count('vacancies'))
        context['companies'] = Company.objects.annotate(num_vacancies=Count('vacancies'))
        return context


class AllVacanciesListView(TemplateView):
    template_name = 'vacancies/vacancies.html'

    def get_context_data(self, **kwargs):
        context = super(AllVacanciesListView, self).get_context_data(**kwargs)
        context['count_of_vacancies'] = Vacancy.objects.count()
        context['vacancies'] = Vacancy.objects.all()
        return context


class SpecializationListView(TemplateView):
    template_name = 'vacancies/specialization.html'

    def get_context_data(self, **kwargs):
        context = super(SpecializationListView, self).get_context_data(**kwargs)
        specialization_id = self.kwargs['specialization_id']
        instance_of_model = get_object_or_404(Specialty, code=specialization_id)
        context['specialization'] = instance_of_model
        context['vacancies'] = instance_of_model.vacancies.all()
        context['count_of_vacancies'] = instance_of_model.vacancies.count()
        return context


class CompanyListView(TemplateView):
    template_name = 'vacancies/company.html'

    def get_context_data(self, **kwargs):
        context = super(CompanyListView, self).get_context_data(**kwargs)
        company_id = self.kwargs['company_id']
        instance_of_model = get_object_or_404(Company, id=company_id)
        context['company'] = instance_of_model
        context['vacancies'] = instance_of_model.vacancies.all()
        context['count_of_vacancies_from_the_company'] = instance_of_model.vacancies.count()
        return context


class VacancyListView(TemplateView):
    template_name = 'vacancies/vacancy.html'

    def get_context_data(self, **kwargs):
        context = super(VacancyListView, self).get_context_data(**kwargs)
        vacancy_id = self.kwargs['vacancy_id']
        instance_of_model = get_object_or_404(Vacancy, id=vacancy_id)
        context['vacancy'] = instance_of_model
        return context


class SignUpView(CreateView):
    form_class = UserCreationForm
    success_url = 'login'
    template_name = 'signup.html'


class LogInView(LoginView):
    redirect_authenticated_user = True
    template_name = 'login.html'


class MyCompany(TemplateView):
    template_name = 'vacancies/company-edit.html'


class MyVacancies(TemplateView):
    template_name = 'vacancies/company-vacancies.html'


def custom_handler404(request, exception):
    return HttpResponseNotFound('Страница не найдена')


def custom_handler500(request):
    return HttpResponseServerError('Внутренняя ошибка сервера')
