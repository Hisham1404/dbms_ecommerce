# Generated by Django 4.2.4 on 2023-11-20 18:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0004_shippingaddress'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customer',
            name='password',
        ),
    ]
