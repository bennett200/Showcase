# Generated by Django 4.2.3 on 2023-07-20 02:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0004_alter_product_description_and_more'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='product',
            unique_together={('title', 'description')},
        ),
    ]