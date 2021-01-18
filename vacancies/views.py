from django.db.models import Count
from django.http import Http404
from django.http import HttpResponseNotFound
from django.http import HttpResponseServerError
from django.views.generic import ListView

from .models import Company
from .models import Specialty
from .models import Vacancy


class MainListView(ListView):
    model = Specialty
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super(MainListView, self).get_context_data(**kwargs)
        context['specialties'] = Specialty.objects.annotate(num_vacancies=Count('vacancies'))
        context['companies'] = Company.objects.annotate(num_vacancies=Count('vacancies'))
        return context


class AllVacanciesListView(ListView):
    model = Vacancy
    template_name = 'vacancies/vacancies.html'

    def get_context_data(self, **kwargs):
        context = super(AllVacanciesListView, self).get_context_data(**kwargs)
        context['count_of_vacancies'] = Vacancy.objects.count()
        context['vacancies'] = Vacancy.objects.all()
        return context


class SpecializationListView(ListView):
    model = Specialty
    template_name = 'vacancies/specialization.html'

    def get_context_data(self, **kwargs):
        context = super(SpecializationListView, self).get_context_data(**kwargs)
        specialization_id = self.kwargs['specialization_id']
        try:
            instance_of_model = Specialty.objects.get(code=specialization_id)
        except Specialty.DoesNotExist:
            raise Http404
        context['specialization'] = instance_of_model
        context['vacancies_by_specialization'] = instance_of_model.vacancies.all()
        context['count_of_vacancies_by_specialization'] = instance_of_model.vacancies.count()
        return context


class CompanyListView(ListView):
    model = Company
    template_name = 'vacancies/company.html'

    def get_context_data(self, **kwargs):
        context = super(CompanyListView, self).get_context_data(**kwargs)
        company_id = self.kwargs['company_id']
        try:
            instance_of_model = Company.objects.get(id=company_id)
        except Company.DoesNotExist:
            raise Http404
        context['company'] = instance_of_model
        context['vacancies'] = instance_of_model.vacancies.all()
        context['count_of_vacancies_from_the_company'] = instance_of_model.vacancies.count()
        return context


class VacancyListView(ListView):
    model = Vacancy
    template_name = 'vacancies/vacancy.html'

    def get_context_data(self, **kwargs):
        context = super(VacancyListView, self).get_context_data(**kwargs)
        vacancy_id = self.kwargs['vacancy_id']
        try:
            instance_of_model = Vacancy.objects.get(id=vacancy_id)
        except Vacancy.DoesNotExist:
            raise Http404
        context['vacancy'] = instance_of_model
        return context


def custom_handler404(request, exception):
    return HttpResponseNotFound('Страница не найдена')


def custom_handler500(request):
    return HttpResponseServerError('Внутренняя ошибка сервера')
