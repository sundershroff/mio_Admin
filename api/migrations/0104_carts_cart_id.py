# Generated by Django 4.0.4 on 2024-04-17 07:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0103_remove_carts_uid'),
    ]

    operations = [
        migrations.AddField(
            model_name='carts',
            name='cart_id',
            field=models.TextField(null=True),
        ),
    ]
