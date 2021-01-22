from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Company(models.Model):
    title = models.CharField(max_length=120)
    location = models.CharField(max_length=120)
    logo = models.URLField(default='https://place-hold.it/100x60')
    description = models.TextField()
    employee_count = models.IntegerField()
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.title


class Specialty(models.Model):
    code = models.CharField(max_length=120)
    title = models.CharField(max_length=120)
    picture = models.URLField(default='https://place-hold.it/100x60')

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
    written_username = models.CharField(max_length=120)
    written_phone = models.CharField(max_length=120)
    written_cover_letter = models.TextField()
    vacancy = models.ForeignKey(Vacancy, on_delete=models.CASCADE, related_name='applications')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='applications')
