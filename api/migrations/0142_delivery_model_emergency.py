# Generated by Django 4.0.4 on 2024-04-29 08:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0141_delivery_model_float_amount'),
    ]

    operations = [
        migrations.AddField(
            model_name='delivery_model',
            name='emergency',
            field=models.BooleanField(default=0),
        ),
    ]
