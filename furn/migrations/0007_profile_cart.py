# Generated by Django 5.0.2 on 2024-02-17 09:26

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('furn', '0006_cart'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='cart',
            field=models.ForeignKey(default='2', on_delete=django.db.models.deletion.CASCADE, to='furn.cart'),
            preserve_default=False,
        ),
    ]
