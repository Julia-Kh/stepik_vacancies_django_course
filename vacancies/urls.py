from django.urls import path

from vacancies.views import AllVacanciesView
from vacancies.views import CompanyView
from vacancies.views import MainView
from vacancies.views import MyCompanyView
from vacancies.views import MyVacanciesView
from vacancies.views import MyVacancyView
from vacancies.views import SendApplicationView
from vacancies.views import SpecializationView
from vacancies.views import VacancyView


urlpatterns = [
    path('', MainView.as_view(), name='main'),
    path('vacancies/', AllVacanciesView.as_view(), name='all_vacancies'),
    path('vacancies/cat/<str:specialization_id>/', SpecializationView.as_view(), name='specialization'),
    path('companies/<int:company_id>/', CompanyView.as_view(), name='company'),
    path('vacancies/<int:vacancy_id>/', VacancyView.as_view(), name='vacancy'),
    path('vacancies/<int:vacancy_id>/send/', SendApplicationView.as_view(), name='send_application'),
    path('mycompany/', MyCompanyView.as_view(), name='my_company'),
    path('mycompany/vacancies/', MyVacanciesView.as_view(), name='my_vacancies'),
    path('mycompany/vacancies/<int:vacancy_id>/', MyVacancyView.as_view(), name='my_vacancy'),
]
