# Generated by Django 4.1.7 on 2023-04-12 09:57

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('dashboard', '0021_customuser_user'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='CustomUser',
            new_name='Profile',
        ),
    ]