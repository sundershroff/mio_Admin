# Generated by Django 4.0.4 on 2024-04-12 10:25

import datetime
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0084_d_original_productsmodel_district'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product_ordermodel',
            name='order_date',
        ),
        migrations.AddField(
            model_name='d_originalmodel',
            name='latitude',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='d_originalmodel',
            name='longitude',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='dailymio_model',
            name='latitude',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='dailymio_model',
            name='longitude',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='foodmodel',
            name='latitude',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='foodmodel',
            name='longitude',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='freshcutsmodel',
            name='latitude',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='freshcutsmodel',
            name='longitude',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='jewellerymodel',
            name='latitude',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='jewellerymodel',
            name='longitude',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='pharmacy_model',
            name='latitude',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='pharmacy_model',
            name='longitude',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='product_ordermodel',
            name='expected_deliverydate',
            field=models.DateField(default=datetime.date(2024, 4, 19), null=True),
        ),
        migrations.AddField(
            model_name='shoppingmodel',
            name='latitude',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='shoppingmodel',
            name='longitude',
            field=models.TextField(null=True),
        ),
        migrations.CreateModel(
            name='Reviews',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.CharField(max_length=240)),
                ('rating', models.FloatField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)])),
                ('d_origin_product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.d_original_productsmodel')),
                ('dailymio_product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.dmio_productsmodel')),
                ('food_product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.food_productsmodel')),
                ('freshcut_product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.fresh_productsmodel')),
                ('jewel_product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.jewel_productsmodel')),
                ('pharmacy_product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.pharmacy_productsmodel')),
                ('shop_product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.shop_productsmodel')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.end_usermodel')),
            ],
        ),
        migrations.CreateModel(
            name='Offers',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('discount', models.TextField(default=0)),
                ('isAvailable', models.BooleanField(default=True)),
                ('start_date', models.DateField(null=True)),
                ('end_date', models.DateField(null=True)),
                ('d_origin_product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.d_original_productsmodel')),
                ('dailymio_product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.dmio_productsmodel')),
                ('food_product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.food_productsmodel')),
                ('freshcut_product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.fresh_productsmodel')),
                ('jewel_product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.jewel_productsmodel')),
                ('pharmacy_product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.pharmacy_productsmodel')),
                ('shop_product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.shop_productsmodel')),
            ],
        ),
        migrations.CreateModel(
            name='Carts',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('qty', models.PositiveIntegerField(default=1)),
                ('d_origin_product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.d_original_productsmodel')),
                ('dailymio_product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.dmio_productsmodel')),
                ('food_product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.food_productsmodel')),
                ('freshcut_product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.fresh_productsmodel')),
                ('jewel_product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.jewel_productsmodel')),
                ('pharmacy_product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.pharmacy_productsmodel')),
                ('shop_product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.shop_productsmodel')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.end_usermodel')),
            ],
        ),
    ]
