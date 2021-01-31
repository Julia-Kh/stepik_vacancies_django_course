from django.urls import path

from vacancies.views.public import AllVacanciesView
from vacancies.views.public import CompanyView
from vacancies.views.public import MainView
from vacancies.views.my_company import MyCompanyCreateView
from vacancies.views.my_company import MyCompanyEditView
from vacancies.views.my_company import MyCompanyLetsStartView
from vacancies.views.my_resume import MyResumeCreateView
from vacancies.views.my_resume import MyResumeEditView
from vacancies.views.my_resume import MyResumeLetsStartView
from vacancies.views.my_company_vacancies import MyVacanciesLetsStartView
from vacancies.views.my_company_vacancies import MyVacanciesView
from vacancies.views.my_company_vacancies import MyVacancyCreateView
from vacancies.views.my_company_vacancies import MyVacancyEditView
from vacancies.views.public import SearchView
from vacancies.views.public import SendApplicationView
from vacancies.views.public import SpecializationView
from vacancies.views.public import VacancyView


urlpatterns = [
    path('', MainView.as_view(), name='main'),
    path('vacancies/', AllVacanciesView.as_view(), name='all_vacancies'),
    path('vacancies/cat/<str:specialization_id>/', SpecializationView.as_view(), name='specialization'),
    path('companies/<int:company_id>/', CompanyView.as_view(), name='company'),
    path('vacancies/<int:vacancy_id>/', VacancyView.as_view(), name='vacancy'),
    path('vacancies/<int:vacancy_id>/send/', SendApplicationView.as_view(), name='send_application'),
    path('mycompany/', MyCompanyEditView.as_view(), name='my_company_and_my_vacancies'),
    path('mycompany/create/', MyCompanyCreateView.as_view(), name='my_company_create'),
    path('mycompany/letsstart/', MyCompanyLetsStartView.as_view(), name='my_company_lets_start'),
    path('mycompany/vacancies/letsstart/', MyVacanciesLetsStartView.as_view(), name='my_vacancies_lets_start'),
    path('mycompany/vacancies/create/', MyVacancyCreateView.as_view(), name='my_vacancy_create'),
    path('mycompany/vacancies/', MyVacanciesView.as_view(), name='my_vacancies'),
    path('mycompany/vacancies/<int:vacancy_id>/', MyVacancyEditView.as_view(), name='my_vacancy'),
    path('myresume/', MyResumeEditView.as_view(), name='my_resume'),
    path('myresume/letsstart/', MyResumeLetsStartView.as_view(), name='my_resume_lets_start'),
    path('myresume/create/', MyResumeCreateView.as_view(), name='my_resume_create'),
    path('search?s=<query>', SearchView.as_view(), name='search'),
]
