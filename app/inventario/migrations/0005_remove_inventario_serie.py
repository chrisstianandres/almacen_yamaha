# Generated by Django 3.1.4 on 2021-01-19 22:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventario', '0004_inventario_venta'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='inventario',
            name='serie',
        ),
    ]