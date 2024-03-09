# Generated by Django 4.2.7 on 2024-01-19 21:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('session', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_cost', models.DecimalField(decimal_places=2, max_digits=10)),
                ('amount_paid', models.DecimalField(decimal_places=2, max_digits=10)),
                ('payment_method', models.CharField(choices=[('cash', 'Cash'), ('online', 'Online'), ('split', 'Split')], max_length=10)),
                ('unpaid_amount', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('amount_paid_cash', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('amount_paid_online', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('payment_status', models.CharField(choices=[('fully_paid', 'Fully Paid'), ('unpaid', 'Unpaid')], default='unpaid', max_length=10)),
                ('session', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='session.session')),
            ],
        ),
    ]