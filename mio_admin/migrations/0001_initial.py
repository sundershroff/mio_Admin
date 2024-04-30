# Generated by Django 5.0 on 2024-04-30 16:00

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('api', '0146_alter_d_original_productsmodel_rating_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='admin_CustomUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.TextField(null=True)),
                ('name', models.TextField(null=True)),
                ('email', models.EmailField(max_length=254, null=True)),
                ('password', models.TextField(null=True)),
                ('phonenumber', models.TextField(null=True)),
                ('access_priveleges', models.JSONField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='banner',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.TextField(null=True)),
                ('banner1', models.ImageField(null=True, upload_to='banner')),
                ('banner2', models.ImageField(null=True, upload_to='banner')),
                ('ad1', models.ImageField(null=True, upload_to='banner')),
                ('ad2', models.ImageField(null=True, upload_to='banner')),
            ],
        ),
        migrations.CreateModel(
            name='business_commision',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('commission', models.TextField(null=True)),
                ('gst', models.TextField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='comission_Editing',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('per_km', models.IntegerField(null=True)),
                ('incentive', models.IntegerField(null=True)),
                ('normal_delivery_commision', models.IntegerField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='hsn_code',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hsn_code', models.TextField(null=True)),
                ('goods', models.TextField(null=True)),
                ('gst', models.TextField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Hub_CustomUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.TextField(null=True)),
                ('name', models.TextField(null=True)),
                ('email', models.EmailField(max_length=254, null=True)),
                ('password', models.TextField(null=True)),
                ('phonenumber', models.TextField(null=True)),
                ('hub', models.TextField(null=True)),
                ('door_no', models.TextField(null=True)),
                ('street', models.TextField(null=True)),
                ('city', models.TextField(null=True)),
                ('state', models.TextField(null=True)),
                ('country', models.TextField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='shutdown',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('shopping', models.BooleanField(default=0, null=True)),
                ('food', models.BooleanField(default=0, null=True)),
                ('fresh_cuts', models.BooleanField(default=0, null=True)),
                ('daily_mio', models.BooleanField(default=0, null=True)),
                ('pharmacy', models.BooleanField(default=0, null=True)),
                ('d_original', models.BooleanField(default=0, null=True)),
                ('jewellery', models.BooleanField(default=0, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='zone',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('zone', models.TextField(null=True)),
                ('pincode', models.JSONField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='admin_to_business_payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('balance_amount', models.FloatField(default=0)),
                ('paid_amount', models.FloatField(default=0)),
                ('seller', models.TextField(null=True)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.product_ordermodel')),
            ],
        ),
    ]
