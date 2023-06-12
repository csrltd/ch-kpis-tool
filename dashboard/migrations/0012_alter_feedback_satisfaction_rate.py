# Generated by Django 4.1.7 on 2023-06-08 08:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0011_alter_feedback_satisfaction_rate'),
    ]

    operations = [
        migrations.AlterField(
            model_name='feedback',
            name='satisfaction_rate',
            field=models.CharField(choices=[('strongly_dissatisfied', '0-10'), ('quite_dissatisfied', '11-30'), ('dissatisfied', '31-50'), ('satisfied', '51-60'), ('quite_satisfied', '61-80'), ('strongly_satisfied', '81-100')], default='strongly_dissatisfied', max_length=21),
        ),
    ]