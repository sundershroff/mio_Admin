# Generated by Django 4.0.4 on 2024-04-20 05:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0112_product_ordermodel_emergency_optional_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='product_ordermodel',
            name='pincode',
            field=models.TextField(null=True),
        ),
    ]