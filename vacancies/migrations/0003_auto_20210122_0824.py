# Generated by Django 3.1.5 on 2021-01-22 05:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vacancies', '0002_auto_20210122_0712'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='logo',
            field=models.ImageField(upload_to='company_images'),
        ),
        migrations.AlterField(
            model_name='specialty',
            name='picture',
            field=models.ImageField(upload_to='speciality_images'),
        ),
    ]
