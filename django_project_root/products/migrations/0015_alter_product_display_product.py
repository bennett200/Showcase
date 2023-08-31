# Generated by Django 4.2.3 on 2023-07-29 17:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0014_product_display_product'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='display_product',
            field=models.BooleanField(choices=[(True, 'Display'), (False, 'Keep Hidden')], default=False, null=True),
        ),
    ]
