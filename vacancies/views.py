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
        return context


class AllVacanciesListView(ListView):
    model = Vacancy
    template_name = 'vacancies/vacancies.html'


class SpecializationListView(ListView):
    model = Specialty
    template_name = 'vacancies/specialization.html'


class CompanyListView(ListView):
    model = Company
    template_name = 'vacancies/company.html'


class VacancyListView(ListView):
    model = Vacancy
    template_name = 'vacancies/vacancy.html'
