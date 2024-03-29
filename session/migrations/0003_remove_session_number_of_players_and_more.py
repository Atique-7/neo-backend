# Generated by Django 4.2.7 on 2024-02-19 05:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('session', '0002_remove_session_admin_duration'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='session',
            name='number_of_players',
        ),
        migrations.AlterField(
            model_name='session',
            name='actual_duration',
            field=models.BigIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='session',
            name='planned_duration',
            field=models.BigIntegerField(blank=True, null=True),
        ),
    ]
