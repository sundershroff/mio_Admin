# Generated by Django 4.0.4 on 2024-04-04 05:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0066_remove_dorigin_ordermodel_business_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='shop_ordermodel',
        ),
    ]
