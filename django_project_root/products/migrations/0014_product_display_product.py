# Generated by Django 4.2.3 on 2023-07-29 17:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0013_alter_categories_description_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='display_product',
            field=models.BooleanField(default=False, null=True),
        ),
    ]
