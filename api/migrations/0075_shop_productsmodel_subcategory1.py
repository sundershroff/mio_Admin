# Generated by Django 4.0.4 on 2024-04-08 04:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0074_d_originalmodel_category_dailymio_model_category_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='shop_productsmodel',
            name='subcategory1',
            field=models.TextField(null=True),
        ),
    ]