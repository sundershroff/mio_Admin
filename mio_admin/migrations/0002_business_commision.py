# Generated by Django 4.0.4 on 2024-04-03 10:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mio_admin', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='business_commision',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('commission', models.TextField(null=True)),
                ('gst', models.TextField(null=True)),
            ],
        ),
    ]