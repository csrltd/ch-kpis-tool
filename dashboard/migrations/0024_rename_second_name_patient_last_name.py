# Generated by Django 4.1.7 on 2023-04-12 11:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0023_rename_patientid_patient_patient_id_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='patient',
            old_name='second_name',
            new_name='last_name',
        ),
    ]