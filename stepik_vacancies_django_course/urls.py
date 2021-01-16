"""stepik_vacancies_django_course URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path

from vacancies.views import AllVacanciesListView
from vacancies.views import MainListView
from vacancies.views import SpecializationListView
from vacancies.views import CompanyListView
from vacancies.views import VacancyListView

urlpatterns = [
    path('', MainListView.as_view()),
    path('vacancies/', AllVacanciesListView.as_view()),
    path('vacancies/cat/<str:specialization_id>/', SpecializationListView.as_view()),
    path('companies/<int:company_id>/', CompanyListView.as_view()),
    path('vacancies/<int:vacancy_id>/', VacancyListView.as_view()),
]
