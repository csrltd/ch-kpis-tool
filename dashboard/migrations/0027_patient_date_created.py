# Generated by Django 4.1.7 on 2023-05-04 08:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0026_alter_patient_birthday'),
    ]

    operations = [
        migrations.AddField(
            model_name='patient',
            name='date_created',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]