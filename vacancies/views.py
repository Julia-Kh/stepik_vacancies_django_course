from django.contrib.auth import get_user_model
from django.db.models import Count
from django.http import HttpResponseNotFound
from django.http import HttpResponseServerError
from django.shortcuts import get_object_or_404, render
from django.shortcuts import redirect
from django.urls import reverse
from django.utils import timezone
from django.views import View
from django.views.generic import TemplateView

from .forms import ApplicationForm
from .forms import CompanyForm
from .forms import VacancyForm
from .models import Application
from .models import Company
from .models import Specialty
from .models import Vacancy


class MainView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super(MainView, self).get_context_data(**kwargs)
        context['specialties'] = Specialty.objects.annotate(num_vacancies=Count('vacancies'))
        context['companies'] = Company.objects.annotate(num_vacancies=Count('vacancies'))
        return context


class AllVacanciesView(TemplateView):
    template_name = 'vacancies/vacancies.html'

    def get_context_data(self, **kwargs):
        context = super(AllVacanciesView, self).get_context_data(**kwargs)
        context['count_of_vacancies'] = Vacancy.objects.count()
        context['vacancies'] = Vacancy.objects.all()
        return context


class SpecializationView(TemplateView):
    template_name = 'vacancies/specialization.html'

    def get_context_data(self, **kwargs):
        context = super(SpecializationView, self).get_context_data(**kwargs)
        specialization_id = self.kwargs['specialization_id']
        instance_of_model = get_object_or_404(Specialty, code=specialization_id)
        context['specialization'] = instance_of_model
        context['vacancies'] = instance_of_model.vacancies.all()
        context['count_of_vacancies'] = instance_of_model.vacancies.count()
        return context


class CompanyView(TemplateView):
    template_name = 'vacancies/company.html'

    def get_context_data(self, **kwargs):
        context = super(CompanyView, self).get_context_data(**kwargs)
        company_id = self.kwargs['company_id']
        instance_of_model = get_object_or_404(Company, id=company_id)
        context['company'] = instance_of_model
        context['vacancies'] = instance_of_model.vacancies.all()
        context['count_of_vacancies_from_the_company'] = instance_of_model.vacancies.count()
        return context


class VacancyView(TemplateView):
    template_name = 'vacancies/vacancy.html'

    def get_context_data(self, **kwargs):
        context = super(VacancyView, self).get_context_data(**kwargs)
        vacancy_id = self.kwargs['vacancy_id']
        instance_of_model = get_object_or_404(Vacancy, id=vacancy_id)
        context['vacancy'] = instance_of_model
        application_form = ApplicationForm()
        application_form.helper.form_action = reverse('vacancy', kwargs={'vacancy_id': vacancy_id})
        context['form'] = application_form
        return context

    def post(self, request, *args, **kwargs):
        username = request.POST.get('username')
        phone = request.POST.get('phone')
        cover_letter = request.POST.get('cover_letter')
        user = get_user_model()
        if request.user:
            username = request.user.username
            user = user.objects.get(username=username)
        else:
            user = user.objects.get(username='Anonymous')
        Application.objects.create(username=username, phone=phone, cover_letter=cover_letter,
                                   vacancy=Vacancy.objects.get(id=self.kwargs['vacancy_id']), user=user)
        return redirect('send_application', vacancy_id=self.kwargs['vacancy_id'])


class MyCompanyEditView(View):

    def get(self, request, *args, **kwargs):
        template_name = 'vacancies/my_company_edit.html'
        user = request.user
        if not user.is_authenticated:
            return redirect('login')
        company = Company.objects.filter(owner=user)
        if company.count() == 0:
            return redirect('my_company_lets_start')
        else:
            company = company[0]
        company_form = CompanyForm(instance=company)
        return render(request, template_name, {'form': company_form})

    def post(self, request, *args, **kwargs):
        company = Company.objects.filter(owner=request.user)[0]
        company_form = CompanyForm(request.POST, instance=company)
        if company_form.is_valid():
            company = company_form.save(commit=False)
            company.owner = request.user
            company.save()
            return redirect('my_company')


class MyCompanyCreateView(View):

    def get(self, request, *args, **kwargs):
        template_name = 'vacancies/my_company_create.html'
        user = request.user
        if not user.is_authenticated:
            return redirect('login')
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
            return redirect('my_company')


class MyCompanyLetsStartView(View):

    def get(self, request, *args, **kwargs):
        template_name = 'vacancies/my_company_and_vacancies_lets_start.html'
        if not request.user.is_authenticated:
            return redirect('login')
        context = {}
        context['text'] = 'Пока мы думаем, что вы – частное лицо. Хотите создать карточку компании, разместить информацию и вакансии?'
        context['button_text'] = 'Создать карточку компании'
        context['button_url'] = reverse('my_company_create')
        context['header_text'] = 'Моя компания'
        return render(request, template_name, context=context)


class MyVacanciesLetsStartView(View):

    def get(self, request, *args, **kwargs):
        template_name = 'vacancies/my_company_and_vacancies_lets_start.html'
        if not request.user.is_authenticated:
            return redirect('login')
        context = {}
        context['text'] = 'У вас пока нет вакансий, но вы можете создать первую!'
        context['button_text'] = 'Добавить вакансию'
        context['button_url'] = reverse('my_vacancy_create')
        context['header_text'] = 'Мои вакансии'
        return render(request, template_name, context=context)


class MyVacancyCreateView(TemplateView):
    template_name = 'vacancies/vacancy_create-edit.html'

    def get_context_data(self, **kwargs):
        context = super(MyVacancyCreateView, self).get_context_data(**kwargs)
        vacancy_form = VacancyForm()
        context['form'] = vacancy_form
        return context

    def post(self, request, *args, **kwargs):
        form = VacancyForm(request.POST)
        if form.is_valid():
            vacancy = form.save(commit=False)
            user = request.user
            company = Company.objects.filter(owner=user)
            vacancy.company = company[0]
            vacancy.posted = timezone.now()
            vacancy.save()
            return redirect('my_vacancy', vacancy_id=vacancy.pk)


class MyVacanciesView(View):

    def get(self, request, *args, **kwargs):
        template_name = 'vacancies/my_vacancies.html'
        user = request.user
        company = Company.objects.filter(owner=user)
        if company.count() == 0:
            return redirect('my_company_lets_start')
        company = company[0]
        vacancies = Vacancy.objects.filter(company=company)
        if not vacancies:
            return redirect('my_vacancies_lets_start')
        context = {}
        context['vacancies'] = vacancies
        return render(request, template_name, context)


class SendApplicationView(TemplateView):
    template_name = 'vacancies/sent.html'

    def get_context_data(self, **kwargs):
        context = super(SendApplicationView, self).get_context_data(**kwargs)
        vacancy_id = self.kwargs['vacancy_id']
        context['back_to_vacancy_url'] = reverse('vacancy', kwargs={'vacancy_id': vacancy_id})
        return context


class MyVacancyEditView(View):

    def get(self, request, *args, **kwargs):
        template_name = 'vacancies/vacancy_create-edit.html'
        vacancy = get_object_or_404(Vacancy, pk=self.kwargs['vacancy_id'])
        vacancy_form = VacancyForm(instance=vacancy)
        return render(request, template_name, {'form': vacancy_form})

    def post(self, request, *args, **kwargs):
        vacancy = get_object_or_404(Vacancy, pk=self.kwargs['vacancy_id'])
        vacancy_form = VacancyForm(request.POST, instance=vacancy)
        if vacancy_form.is_valid():
            vacancy = vacancy_form.save(commit=False)
            user = request.user
            company = Company.objects.filter(owner=user)
            vacancy.company = company[0]
            vacancy.posted = timezone.now()
            vacancy.save()
            return redirect('my_vacancy', vacancy_id=vacancy.pk)


def custom_handler404(request, exception):
    return HttpResponseNotFound('Страница не найдена')


def custom_handler500(request):
    return HttpResponseServerError('Внутренняя ошибка сервера')
