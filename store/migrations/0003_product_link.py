# Generated by Django 5.0.4 on 2024-04-29 00:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0002_product_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='link',
            field=models.CharField(max_length=200, null=True),
        ),
    ]
