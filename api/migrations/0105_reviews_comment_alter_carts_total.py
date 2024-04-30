# Generated by Django 4.0.4 on 2024-04-17 10:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0104_carts_cart_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='reviews',
            name='comment',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='carts',
            name='total',
            field=models.FloatField(blank=True, null=True),
        ),
    ]