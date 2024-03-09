# Generated by Django 4.2.7 on 2024-03-06 17:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('session', '0006_alter_pricing_duration_minutes_and_more'),
        ('food', '0001_initial'),
        ('transactions', '0003_transaction_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='food',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='transaction',
            name='food_sale',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='food.sale'),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='session',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='session.session'),
        ),
    ]
