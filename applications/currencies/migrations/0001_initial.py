# Generated by Django 5.0.6 on 2024-05-19 10:25

import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Currency',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('code', models.CharField(max_length=3)),
                ('symbol', models.CharField(max_length=5)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='CurrencyRate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rate', models.DecimalField(decimal_places=4, max_digits=10)),
                ('rate_type', models.CharField(choices=[('sell', 'Sell'), ('buy', 'Buy')], max_length=5)),
                ('date', models.DateField()),
                ('currency', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rates', to='currencies.currency')),
            ],
        ),
    ]