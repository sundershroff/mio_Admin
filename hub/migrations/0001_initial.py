# Generated by Django 5.0 on 2024-04-30 09:28

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('api', '0144_d_original_productsmodel_rating_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='product_arrive',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_picked', models.BooleanField(default=0)),
                ('product_picked_date', models.DateTimeField(null=True)),
                ('product_arrived', models.BooleanField(default=0)),
                ('product_arrived_date', models.DateTimeField(null=True)),
                ('product_arrived_to_me', models.BooleanField(default=0)),
                ('product_arrived_to_me_date', models.DateTimeField(null=True)),
                ('delivery_person', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='api.delivery_model')),
                ('order', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='api.product_ordermodel')),
            ],
        ),
    ]