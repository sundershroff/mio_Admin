# Generated by Django 4.0.4 on 2024-04-09 12:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0081_product_ordermodel_d_id_product_ordermodel_dmio_id_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='product_ordermodel',
            name='business',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='api.businessmodel'),
        ),
    ]
