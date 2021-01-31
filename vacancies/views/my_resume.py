from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.shortcuts import redirect
from django.views import View

from vacancies.forms import ResumeForm
from vacancies.models import Resume


class MyResumeEditView(View):

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        try:
            request.user.resume
        except Resume.DoesNotExist:
            return redirect('my_resume_lets_start')
        template_name = 'vacancies/my_resume/my_resume_create-edit.html'
        resume = get_object_or_404(Resume, user=request.user)
        resume_form = ResumeForm(instance=resume)
        return render(request, template_name, {'form': resume_form})

    def post(self, request, *args, **kwargs):
        resume = get_object_or_404(Resume, user=request.user)
        resume_form = ResumeForm(request.POST, instance=resume)
        if resume_form.is_valid():
            resume = resume_form.save(commit=False)
            resume.user = request.user
            resume.save()
            return redirect('my_resume')


class MyResumeCreateView(View):

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        try:
            request.user.resume
            return redirect('my_resume')
        except Resume.DoesNotExist:
            template_name = 'vacancies/my_resume/my_resume_create-edit.html'
            context = {}
            resume_form = ResumeForm()
            context['form'] = resume_form
            return render(request, template_name, context=context)

    def post(self, request, *args, **kwargs):
        resume_form = ResumeForm(request.POST)
        if resume_form.is_valid():
            resume = resume_form.save(commit=False)
            resume.user = request.user
            resume.save()
            return redirect('my_resume')


class MyResumeLetsStartView(View):

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        try:
            request.user.resume
        except Resume.DoesNotExist:
            template_name = 'vacancies/my_resume/my_resume_lets_start.html'
            return render(request, template_name=template_name)
        return redirect('my_resume')
