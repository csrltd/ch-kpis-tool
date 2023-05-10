from django.contrib.auth.models import Group
from django.db import migrations


def create_groups(apps, schema_editor):
    admin_group = Group.objects.create(name='Admin')
    ceo_group = Group.objects.create(name='CEO')
    hospital_admin_group = Group.objects.create(name='Hospital Admin')
    employee_group = Group.objects.create(name='Employee')


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_groups),
    ]
