from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models


User = get_user_model()


class Company(models.Model):
    title = models.CharField(max_length=120)
    location = models.CharField(max_length=120)
    logo = models.ImageField(upload_to=settings.MEDIA_COMPANY_IMAGE_DIR, null=True, blank=True)
    description = models.TextField()
    employee_count = models.IntegerField()
    owner = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.title


class Specialty(models.Model):
    code = models.CharField(max_length=120)
    title = models.CharField(max_length=120)
    picture = models.ImageField(upload_to=settings.MEDIA_SPECIALITY_IMAGE_DIR)

    def __str__(self):
        return self.title


class Vacancy(models.Model):
    title = models.CharField(max_length=120)
    specialty = models.ForeignKey(Specialty, on_delete=models.CASCADE, related_name='vacancies')
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='vacancies')
    skills = models.TextField()
    description = models.TextField()
    salary_from = models.IntegerField()
    salary_to = models.IntegerField()
    posted = models.DateTimeField()

    def __str__(self):
        return self.title


class Application(models.Model):
    username = models.CharField(max_length=120)
    phone = models.CharField(max_length=120)
    cover_letter = models.TextField()
    vacancy = models.ForeignKey(Vacancy, on_delete=models.CASCADE, related_name='applications')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='applications')

    def __str__(self):
        return self.username


class Resume(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=120)
    surname = models.CharField(max_length=120)
    status_choice = [('no', 'Не ищу работу'),
                     ('maybe', 'Рассматриваю предложения'),
                     ('yes', 'Ищу работу'),
                     ]
    status = models.CharField(max_length=5, choices=status_choice)
    salary = models.IntegerField()
    specialty = models.ForeignKey(Specialty, on_delete=models.SET_NULL, null=True, blank=True)
    grade_choice = [('intern', 'Intern'),
                    ('junior', 'Junior'),
                    ('middle', 'Middle'),
                    ('senior', 'Senior'),
                    ('lead', 'Lead'),
                    ]
    grade = models.CharField(max_length=6, choices=grade_choice)
    education = models.TextField()
    experience = models.TextField()
    portfolio = models.URLField()

    def __str__(self):
        return self.name
