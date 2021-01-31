from django.shortcuts import render
from django.shortcuts import redirect
from django.urls import reverse
from django.views import View

from vacancies.forms import CompanyForm
from vacancies.models import Company


class MyCompanyEditView(View):

    def get(self, request, *args, **kwargs):
        template_name = 'vacancies/my_company_and_my_vacancies/my_company_create-edit.html'
        user = request.user
        if not user.is_authenticated:
            return redirect('login')
        try:
            company = user.company
        except Company.DoesNotExist:
            return redirect('my_company_lets_start')
        company_form = CompanyForm(instance=company)
        return render(request, template_name, {'form': company_form})

    def post(self, request, *args, **kwargs):
        company = request.user.company
        company_form = CompanyForm(request.POST, instance=company)
        if company_form.is_valid():
            company = company_form.save(commit=False)
            company.owner = request.user
            company.save()
            return redirect('my_company_and_my_vacancies')


class MyCompanyCreateView(View):

    def get(self, request, *args, **kwargs):
        template_name = 'vacancies/my_company_and_my_vacancies/my_company_create-edit.html'
        user = request.user
        if not user.is_authenticated:
            return redirect('login')
        try:
            request.user.company
            return redirect('my_company_and_my_vacancies')
        except Company.DoesNotExist:
            company_form = CompanyForm()
            context = {}
            context['form'] = company_form
            return render(request, template_name, context=context)

    def post(self, request, *args, **kwargs):
        form = CompanyForm(request.POST)
        if form.is_valid():
            company = form.save(commit=False)
            company.owner = request.user
            company.save()
            return redirect('my_company_and_my_vacancies')


class MyCompanyLetsStartView(View):

    def get(self, request, *args, **kwargs):
        template_name = 'vacancies/my_company_and_my_vacancies/my_company_and_vacancies_lets_start.html'
        if not request.user.is_authenticated:
            return redirect('login')
        try:
            request.user.company
            return redirect('my_company_and_my_vacancies')
        except Company.DoesNotExist:
            context = {}
            context['text'] = 'Пока мы думаем, что вы – частное лицо. Хотите создать карточку компании, ' \
                              'разместить информацию и вакансии?'
            context['button_text'] = 'Создать карточку компании'
            context['button_url'] = reverse('my_company_create')
            context['header_text'] = 'Моя компания'
            return render(request, template_name, context=context)
