# Generated by Django 4.1.7 on 2023-04-10 08:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0011_hospital_covid_vaccination'),
    ]

    operations = [
        migrations.AddField(
            model_name='hospital',
            name='pressure_ulcers',
            field=models.CharField(max_length=255, null=True),
        ),
    ]