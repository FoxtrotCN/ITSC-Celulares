# Generated by Django 5.0.7 on 2024-07-25 19:52

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('itsc_celulares', '0003_remove_customer_device_remove_repairorder_customer_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='repairorder',
            name='technician',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='itsc_celulares.technician'),
        ),
    ]
