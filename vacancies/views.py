from django.contrib.auth.views import LoginView
from django.db.models import Count
from django.http import HttpResponseNotFound
from django.http import HttpResponseServerError
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.views.generic import TemplateView

from .forms import SignUpForm
from .models import Company
from .models import Specialty
from .models import Vacancy


class MainView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super(MainView, self).get_context_data(**kwargs)
        context['specialties'] = Specialty.objects.annotate(num_vacancies=Count('vacancies'))
        context['companies'] = Company.objects.annotate(num_vacancies=Count('vacancies'))
        return context


class AllVacanciesView(TemplateView):
    template_name = 'vacancies/vacancies.html'

    def get_context_data(self, **kwargs):
        context = super(AllVacanciesView, self).get_context_data(**kwargs)
        context['count_of_vacancies'] = Vacancy.objects.count()
        context['vacancies'] = Vacancy.objects.all()
        return context


class SpecializationView(TemplateView):
    template_name = 'vacancies/specialization.html'

    def get_context_data(self, **kwargs):
        context = super(SpecializationView, self).get_context_data(**kwargs)
        specialization_id = self.kwargs['specialization_id']
        instance_of_model = get_object_or_404(Specialty, code=specialization_id)
        context['specialization'] = instance_of_model
        context['vacancies'] = instance_of_model.vacancies.all()
        context['count_of_vacancies'] = instance_of_model.vacancies.count()
        return context


class CompanyView(TemplateView):
    template_name = 'vacancies/company.html'

    def get_context_data(self, **kwargs):
        context = super(CompanyView, self).get_context_data(**kwargs)
        company_id = self.kwargs['company_id']
        instance_of_model = get_object_or_404(Company, id=company_id)
        context['company'] = instance_of_model
        context['vacancies'] = instance_of_model.vacancies.all()
        context['count_of_vacancies_from_the_company'] = instance_of_model.vacancies.count()
        return context


class VacancyView(TemplateView):
    template_name = 'vacancies/vacancy.html'

    def get_context_data(self, **kwargs):
        context = super(VacancyView, self).get_context_data(**kwargs)
        vacancy_id = self.kwargs['vacancy_id']
        instance_of_model = get_object_or_404(Vacancy, id=vacancy_id)
        context['vacancy'] = instance_of_model
        return context


def sign_up_view(request):
    data = {}
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            data['form'] = form
            return render(request, 'signup.html', data)
    else:
        form = SignUpForm()
        data['form'] = form
        return render(request, 'signup.html', data)


class LogInView(LoginView):
    redirect_authenticated_user = True
    template_name = 'login.html'


class MyCompanyView(TemplateView):
    template_name = 'vacancies/company-edit.html'


class MyVacanciesView(TemplateView):
    template_name = 'vacancies/company-vacancies.html'


class SendApplicationView(TemplateView):
    template_name = 'vacancies/sent.html'


class MyVacancyView(TemplateView):
    template_name = 'vacancies/vacancy-edit.html'


def custom_handler404(request, exception):
    return HttpResponseNotFound('Страница не найдена')


def custom_handler500(request):
    return HttpResponseServerError('Внутренняя ошибка сервера')
