# Generated by Django 4.1.7 on 2023-04-10 08:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0009_hospital_hospitalid'),
    ]

    operations = [
        migrations.AddField(
            model_name='hospital',
            name='mortality_rate',
            field=models.CharField(max_length=4, null=True),
        ),
    ]