# Generated by Django 4.0.5 on 2023-07-29 09:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('request_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='currency',
            field=models.CharField(max_length=3),
        ),
    ]
