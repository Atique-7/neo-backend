# Generated by Django 4.2.7 on 2024-02-29 10:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('session', '0003_remove_session_number_of_players_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='pricing',
            name='duration_minutes',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='pricing',
            name='price_per_frame',
            field=models.DecimalField(decimal_places=2, max_digits=6, null=True),
        ),
        migrations.AddField(
            model_name='session',
            name='end_time',
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name='pricing',
            name='session_type',
            field=models.CharField(choices=[('PS5', 'PS5'), ('PS4', 'PS4'), ('Pool', 'Pool'), ('PoolFrame', 'PoolFrame'), ('Snooker', 'Snooker'), ('SnookerFrame', 'SnookerFrame')], max_length=50, unique=True),
        ),
        migrations.AlterField(
            model_name='session',
            name='session_type',
            field=models.CharField(choices=[('PS5', 'PS5'), ('PS4', 'PS4'), ('Pool', 'Pool'), ('PoolFrame', 'PoolFrame'), ('Snooker', 'Snooker'), ('SnookerFrame', 'SnookerFrame')], max_length=50),
        ),
    ]
