# Generated by Django 3.1.4 on 2021-05-22 18:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('compra', '0005_auto_20210522_1251'),
    ]

    operations = [
        migrations.AlterField(
            model_name='compra',
            name='comprobante',
            field=models.CharField(default=1, max_length=100),
        ),
    ]
