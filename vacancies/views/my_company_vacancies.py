from django.http import Http404
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.shortcuts import redirect
from django.urls import reverse
from django.utils import timezone
from django.views import View

from vacancies.forms import VacancyForm
from vacancies.models import Company
from vacancies.models import Vacancy


class MyVacanciesLetsStartView(View):

    def get(self, request, *args, **kwargs):
        template_name = 'vacancies/my_company_and_my_vacancies/my_company_and_vacancies_lets_start.html'
        if not request.user.is_authenticated:
            return redirect('login')
        user_vacancies = Vacancy.objects.filter(company=request.user.company)
        if user_vacancies.count() > 0:
            return redirect('my_vacancies')
        context = {}
        context['text'] = 'У вас пока нет вакансий, но вы можете создать первую!'
        context['button_text'] = 'Добавить вакансию'
        context['button_url'] = reverse('my_vacancy_create')
        context['header_text'] = 'Мои вакансии'
        return render(request, template_name, context=context)


class MyVacancyCreateView(View):

    def get(self, request, *args, **kwargs):
        template_name = 'vacancies/my_company_and_my_vacancies/my_vacancy_create-edit.html'
        if not request.user.is_authenticated:
            return redirect('login')
        try:
            request.user.company
        except Company.DoesNotExist:
            return redirect('my_company_lets_start')
        context = {}
        vacancy_form = VacancyForm()
        context['form'] = vacancy_form
        return render(request, template_name, context=context)

    def post(self, request, *args, **kwargs):
        form = VacancyForm(request.POST)
        if form.is_valid():
            vacancy = form.save(commit=False)
            vacancy.company = request.user.company
            vacancy.posted = timezone.now()
            vacancy.save()
            return redirect('my_vacancy', vacancy_id=vacancy.pk)


class MyVacanciesView(View):

    def get(self, request, *args, **kwargs):
        user = request.user
        if not user.is_authenticated:
            return redirect('login')
        template_name = 'vacancies/my_company_and_my_vacancies/my_vacancies.html'
        try:
            company = user.company
        except Company.DoesNotExist:
            return redirect('my_company_lets_start')
        vacancies = Vacancy.objects.filter(company=company)
        if not vacancies:
            return redirect('my_vacancies_lets_start')
        context = {}
        context['vacancies'] = vacancies
        return render(request, template_name, context)


class MyVacancyEditView(View):

    def get(self, request, *args, **kwargs):
        user = request.user
        if not user.is_authenticated:
            return redirect('login')
        try:
            user.company
        except Company.DoesNotExist:
            return redirect('my_company_lets_start')
        template_name = 'vacancies/my_company_and_my_vacancies/my_vacancy_create-edit.html'
        vacancy = get_object_or_404(Vacancy, pk=self.kwargs['vacancy_id'])
        if vacancy.company.owner.pk != user.pk:
            raise Http404
        vacancy_form = VacancyForm(instance=vacancy)
        return render(request, template_name, {'form': vacancy_form})

    def post(self, request, *args, **kwargs):
        vacancy = get_object_or_404(Vacancy, pk=self.kwargs['vacancy_id'])
        vacancy_form = VacancyForm(request.POST, instance=vacancy)
        if vacancy_form.is_valid():
            vacancy = vacancy_form.save(commit=False)
            vacancy.company = request.user.company
            vacancy.posted = timezone.now()
            vacancy.save()
            return redirect('my_vacancy', vacancy_id=vacancy.pk)
