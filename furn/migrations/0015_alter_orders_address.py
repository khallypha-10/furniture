# Generated by Django 5.0.2 on 2024-02-27 12:55

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('furn', '0014_address'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orders',
            name='address',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='furn.address'),
        ),
    ]
