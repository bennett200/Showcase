# Generated by Django 4.2.3 on 2023-08-09 04:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0041_alter_customerprofile_customer'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customerprofile',
            name='bio',
        ),
        migrations.RemoveField(
            model_name='customerprofile',
            name='first_name',
        ),
        migrations.RemoveField(
            model_name='customerprofile',
            name='last_name',
        ),
        migrations.RemoveField(
            model_name='customerprofile',
            name='profile_img',
        ),
    ]
