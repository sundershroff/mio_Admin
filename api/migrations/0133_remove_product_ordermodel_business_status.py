# Generated by Django 4.0.4 on 2024-04-26 10:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0132_product_ordermodel_ready_to_pick_up'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product_ordermodel',
            name='business_status',
        ),
    ]
