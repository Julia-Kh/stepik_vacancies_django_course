from django.urls import path

from vacancies.views import AllVacanciesListView
from vacancies.views import CompanyListView
from vacancies.views import MainListView
from vacancies.views import SpecializationListView
from vacancies.views import VacancyListView


urlpatterns = [
    path('', MainListView.as_view(), name='main'),
    path('vacancies/', AllVacanciesListView.as_view(), name='all_vacancies'),
    path('vacancies/cat/<str:specialization_id>/', SpecializationListView.as_view()),
    path('companies/<int:company_id>/', CompanyListView.as_view()),
    path('vacancies/<int:vacancy_id>/', VacancyListView.as_view()),
]
