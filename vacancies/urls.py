from django.urls import path

from vacancies.views import AllVacanciesListView
from vacancies.views import CompanyListView
from vacancies.views import MainListView
from vacancies.views import MyCompany
from vacancies.views import MyVacancies
from vacancies.views import SpecializationListView
from vacancies.views import VacancyListView


urlpatterns = [
    path('', MainListView.as_view(), name='main'),
    path('vacancies/', AllVacanciesListView.as_view(), name='all_vacancies'),
    path('vacancies/cat/<str:specialization_id>/', SpecializationListView.as_view(), name='specialization'),
    path('companies/<int:company_id>/', CompanyListView.as_view(), name='company'),
    path('vacancies/<int:vacancy_id>/', VacancyListView.as_view(), name='vacancy'),
    path('mycompany/', MyCompany.as_view(), name='my_company'),
    path('mycompany/vacancies/', MyVacancies.as_view(), name='my_vacancies'),
]
