# Generated by Django 4.0.4 on 2024-04-07 14:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0072_product_ordermodel_product_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='product_ordermodel',
            name='d_id',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='product_ordermodel',
            name='dmio_id',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='product_ordermodel',
            name='food_id',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='product_ordermodel',
            name='fresh_id',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='product_ordermodel',
            name='jewel_id',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='product_ordermodel',
            name='pharm_id',
            field=models.TextField(null=True),
        ),
    ]