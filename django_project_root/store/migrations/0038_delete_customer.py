# Generated by Django 4.2.3 on 2023-08-07 21:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0037_alter_orderitem_notes'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Customer',
        ),
    ]
