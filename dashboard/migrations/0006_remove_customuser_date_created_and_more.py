# Generated by Django 4.1.7 on 2023-04-04 16:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0005_customuser_email_customuser_first_name_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='date_created',
        ),
        migrations.RemoveField(
            model_name='customuser',
            name='department',
        ),
        migrations.RemoveField(
            model_name='customuser',
            name='hospital',
        ),
        migrations.RemoveField(
            model_name='customuser',
            name='role',
        ),
    ]
