# Generated by Django 4.1.7 on 2023-04-04 14:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0003_remove_customuser_email_remove_customuser_first_name_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='user',
        ),
    ]
