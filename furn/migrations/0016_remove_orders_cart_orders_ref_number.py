# Generated by Django 5.0.2 on 2024-02-27 14:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('furn', '0015_alter_orders_address'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orders',
            name='cart',
        ),
        migrations.AddField(
            model_name='orders',
            name='ref_number',
            field=models.CharField(default='12', max_length=50),
            preserve_default=False,
        ),
    ]
