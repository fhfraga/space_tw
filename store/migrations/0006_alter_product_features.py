# Generated by Django 5.0.4 on 2024-09-10 00:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0005_product_features'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='features',
            field=models.CharField(blank=True, default='Nenhuma', max_length=255),
        ),
    ]
