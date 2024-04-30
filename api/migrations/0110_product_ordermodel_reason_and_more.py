# Generated by Django 4.0.4 on 2024-04-19 03:48

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0109_alter_reviews_d_origin_product_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='product_ordermodel',
            name='reason',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='product_ordermodel',
            name='expected_deliverydate',
            field=models.DateField(default=datetime.date(2024, 4, 26), null=True),
        ),
    ]