# Generated by Django 5.0 on 2024-03-27 12:36

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='comission_Editing',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('per_km', models.IntegerField(null=True)),
                ('incentive', models.IntegerField(null=True)),
            ],
        ),
    ]