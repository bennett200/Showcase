# Generated by Django 4.2.3 on 2023-07-19 02:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='categories',
            options={'verbose_name_plural': 'Categories'},
        ),
        migrations.AlterModelOptions(
            name='productcreate',
            options={'verbose_name_plural': 'Product Creation'},
        ),
        migrations.RemoveField(
            model_name='categories',
            name='amount_of_categories',
        ),
    ]
