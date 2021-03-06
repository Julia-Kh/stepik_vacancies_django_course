from django.db.models import Count
from django.db.models import Q
from django.http import HttpResponseNotFound
from django.http import HttpResponseServerError
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import TemplateView

from vacancies.forms import ApplicationForm
from vacancies.models import Company
from vacancies.models import Specialty
from vacancies.models import Vacancy


class MainView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super(MainView, self).get_context_data(**kwargs)
        context['specialties'] = Specialty.objects.annotate(num_vacancies=Count('vacancies'))
        context['companies'] = Company.objects.annotate(num_vacancies=Count('vacancies'))
        return context


class AllVacanciesView(TemplateView):
    template_name = 'vacancies/public/vacancies.html'

    def get_context_data(self, **kwargs):
        context = super(AllVacanciesView, self).get_context_data(**kwargs)
        context['vacancies'] = Vacancy.objects.all()
        context['count_of_vacancies'] = len(context['vacancies'])
        return context


class SpecializationView(TemplateView):
    template_name = 'vacancies/public/specialization.html'

    def get_context_data(self, **kwargs):
        context = super(SpecializationView, self).get_context_data(**kwargs)
        specialization_id = self.kwargs['specialization_id']
        specialty = get_object_or_404(Specialty, code=specialization_id)
        context['specialization'] = specialty
        context['vacancies'] = specialty.vacancies.all()
        context['count_of_vacancies'] = len(context['vacancies'])
        return context


class CompanyView(TemplateView):
    template_name = 'vacancies/public/company.html'

    def get_context_data(self, **kwargs):
        context = super(CompanyView, self).get_context_data(**kwargs)
        company_id = self.kwargs['company_id']
        company = get_object_or_404(Company, id=company_id)
        context['company'] = company
        context['vacancies'] = company.vacancies.all()
        context['count_of_vacancies_from_the_company'] = len(context['vacancies'])
        return context


@method_decorator(login_required, name='post')
class VacancyView(TemplateView):
    template_name = 'vacancies/public/vacancy.html'
    form_class = ApplicationForm

    def get_context_data(self, **kwargs):
        context = super(VacancyView, self).get_context_data(**kwargs)
        vacancy_id = self.kwargs['vacancy_id']
        vacancy = get_object_or_404(Vacancy, id=vacancy_id)
        context['vacancy'] = vacancy
        application_form = ApplicationForm()
        application_form.helper.form_action = reverse_lazy('vacancy', kwargs={'vacancy_id': vacancy_id})
        context['form'] = application_form
        return context

    def post(self, request, vacancy_id, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            application = form.save(commit=False)
            application.user = request.user
            application.vacancy_id = vacancy_id
            application.save()
            return redirect('send_application', vacancy_id=vacancy_id)  # редирект в случае валидной формы
        return self.render_to_response(self.get_context_data(form=form))
        # рендер формы с ошибками в шаблон в случае невалидной формы


class SendApplicationView(TemplateView):
    template_name = 'vacancies/public/sent.html'

    def get_context_data(self, **kwargs):
        context = super(SendApplicationView, self).get_context_data(**kwargs)
        vacancy_id = self.kwargs['vacancy_id']
        context['back_to_vacancy_url'] = reverse_lazy('vacancy', kwargs={'vacancy_id': vacancy_id})
        return context


class SearchView(View):

    def get(self, request, *args, **kwargs):
        template_name = 'vacancies/public/search.html'
        context = {}
        search_input = request.GET.get("search_input")
        context['search_input'] = search_input
        context['vacancies'] = Vacancy.objects.filter(
            Q(title__icontains=search_input) | Q(description__icontains=search_input))
        context['count_of_vacancies'] = context['vacancies'].count()
        return render(request, template_name=template_name, context=context)


def custom_handler404(request, exception):
    return HttpResponseNotFound('Страница не найдена')


def custom_handler500(request):
    return HttpResponseServerError('Внутренняя ошибка сервера')
