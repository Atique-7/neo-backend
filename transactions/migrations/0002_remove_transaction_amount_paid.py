# Generated by Django 4.2.7 on 2024-02-29 10:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='transaction',
            name='amount_paid',
        ),
    ]