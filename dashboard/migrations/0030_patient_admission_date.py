# Generated by Django 4.1.7 on 2023-05-04 08:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0029_patient_date_created'),
    ]

    operations = [
        migrations.AddField(
            model_name='patient',
            name='admission_date',
            field=models.DateTimeField(null=True),
        ),
    ]
