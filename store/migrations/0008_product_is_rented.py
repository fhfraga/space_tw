# Generated by Django 5.0.4 on 2024-10-01 20:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0007_product_available_from_product_available_to'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='is_rented',
            field=models.BooleanField(default=False),
        ),
    ]