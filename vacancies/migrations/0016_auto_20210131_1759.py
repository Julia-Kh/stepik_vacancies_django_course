# Generated by Django 3.1.5 on 2021-01-31 14:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vacancies', '0015_auto_20210131_1500'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='logo',
            field=models.ImageField(blank=True, default=None, upload_to='company_images'),
        ),
    ]
