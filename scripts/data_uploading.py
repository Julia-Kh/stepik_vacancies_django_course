from vacancies.models import Company
from vacancies.models import Specialty
from vacancies.models import Vacancy

from .data import companies
from .data import jobs
from .data import specialties


def change_inf_about_skills(skills):
    lst_with_skills = skills.split(', ')
    dot = ' • '
    return dot.join(lst_with_skills)


def run():
    for company in companies:
        company['id'] = int(company['id'])
        company['employee_count'] = int(company['employee_count'])
        Company.objects.create(**company)

    for specialty in specialties:
        Specialty.objects.create(**specialty)

    for vacancy in jobs:
        specialty_of_vacancy = Specialty.objects.get(code=vacancy['specialty'])
        company_of_vacancy = Company.objects.get(id=int(vacancy['company']))
        vacancy['specialty'] = specialty_of_vacancy
        vacancy['company'] = company_of_vacancy
        vacancy['salary_from'] = int(vacancy['salary_from'])
        vacancy['salary_to'] = int(vacancy['salary_to'])
        vacancy['skills'] = change_inf_about_skills(vacancy['skills'])
        Vacancy.objects.create(**vacancy)
