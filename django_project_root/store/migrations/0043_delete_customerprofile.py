# Generated by Django 4.2.3 on 2023-08-09 04:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0042_remove_customerprofile_bio_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='CustomerProfile',
        ),
    ]