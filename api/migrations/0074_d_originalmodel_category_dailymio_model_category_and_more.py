# Generated by Django 4.0.4 on 2024-04-07 16:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0073_product_ordermodel_d_id_product_ordermodel_dmio_id_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='d_originalmodel',
            name='category',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='dailymio_model',
            name='category',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='foodmodel',
            name='category',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='freshcutsmodel',
            name='category',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='jewellerymodel',
            name='category',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='pharmacy_model',
            name='category',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='shoppingmodel',
            name='category',
            field=models.TextField(null=True),
        ),
    ]
