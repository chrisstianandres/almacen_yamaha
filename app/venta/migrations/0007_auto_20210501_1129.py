# Generated by Django 3.1.4 on 2021-05-01 16:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('venta', '0006_detalle_venta_p_venta_actual'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='venta',
            options={'ordering': ['fecha_venta'], 'verbose_name': 'venta', 'verbose_name_plural': 'ventas'},
        ),
    ]