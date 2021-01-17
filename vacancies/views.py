from django.views.generic import ListView
from .models import Specialty
from .models import Company
from .models import Vacancy


class MainListView(ListView):
    model = Specialty
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super(MainListView, self).get_context_data(**kwargs)
        context['specialties'] = Specialty.objects.all()
        context['count_of_specialties'] = Specialty.objects.count()
        context['companies'] = Company.objects.all()
        context['count_of_companies'] = Company.objects.count()
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
        instance_of_model = Specialty.objects.get(code=specialization_id)
        context['specialization'] = instance_of_model
        context['vacancies_by_specialization'] = instance_of_model.vacancies.all()
        context['count_of_vacancies_by_specialization'] = instance_of_model.vacancies.count()
        return context


class CompanyListView(ListView):
    model = Company
    template_name = 'vacancies/company.html'


class VacancyListView(ListView):
    model = Vacancy
    template_name = 'vacancies/vacancy.html'
