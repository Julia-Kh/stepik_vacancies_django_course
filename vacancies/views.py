from django.contrib.auth.views import LoginView
from django.db.models import Count
from django.http import HttpResponseNotFound
from django.http import HttpResponseServerError
from django.shortcuts import get_object_or_404, render
from django.shortcuts import redirect
from django.views import View
from django.views.generic import TemplateView
from django.views.generic import CreateView
from django.urls import reverse
from django.contrib.auth import get_user_model

from .forms import SignUpForm
from .forms import ApplicationForm
from .forms import CompanyForm
from .models import Company
from .models import Specialty
from .models import Vacancy
from .models import Application


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
        User = get_user_model()
        if request.user:
            username = request.user.username
            user = User.objects.get(username=username)
        else:
            user = User.objects.get(username='Anonymous')
        Application.objects.create(username=username, phone=phone, cover_letter=cover_letter, vacancy=Vacancy.objects.get(id=self.kwargs['vacancy_id']), user=user)
        return redirect('send_application', vacancy_id=self.kwargs['vacancy_id'])


class SignupView(CreateView):
    form_class = SignUpForm
    success_url = '/login'
    template_name = 'signup.html'


class LogInView(LoginView):
    redirect_authenticated_user = True
    template_name = 'login.html'


class MyCompanyEditView(View):

    def get(self, request, *args, **kwargs):
        template_name = 'vacancies/company-edit.html'
        user = request.user
        if not user.is_authenticated:
            raise HttpResponseNotFound
        companies = Company.objects.filter(owner=user)
        if companies.count() == 0:
            return redirect('my_company_lets_start')
        else:
            company_form = CompanyForm()
            context = {}
            context['form'] = company_form
            return render(request, template_name, context=context)


class MyCompanyCreateView(TemplateView):
    template_name = 'vacancies/company-create.html'

    def get_context_data(self, **kwargs):
        context = super(MyCompanyCreateView, self).get_context_data(**kwargs)
        company_form = CompanyForm()
        context['form'] = company_form
        return context

    def post(self, request, *args, **kwargs):
        title = request.POST.get('title')
        location = request.POST.get('location')
        logo = request.POST.get('logo')
        description = request.POST.get('description')
        employee_count = request.POST.get('employee_count')
        User = get_user_model()
        if request.user:
            username = request.user.username
            user = User.objects.get(username=username)
        else:
            user = User.objects.get(username='Anonymous')
        Company.objects.create(title=title, location=location, logo=logo, description=description,
                               employee_count=employee_count, owner=user)
        return redirect('my_company')


class MyCompanyLetsStartView(TemplateView):
    template_name = 'vacancies/company-lets-start.html'


class MyVacanciesView(TemplateView):
    template_name = 'vacancies/company-vacancies.html'


class SendApplicationView(TemplateView):
    template_name = 'vacancies/sent.html'


class MyVacancyView(TemplateView):
    template_name = 'vacancies/vacancy-edit.html'


def custom_handler404(request, exception):
    return HttpResponseNotFound('Страница не найдена')


def custom_handler500(request):
    return HttpResponseServerError('Внутренняя ошибка сервера')
