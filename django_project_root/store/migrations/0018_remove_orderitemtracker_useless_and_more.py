# Generated by Django 4.2.3 on 2023-08-03 07:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0017_orderitemtracker_useless'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orderitemtracker',
            name='useless',
        ),
        migrations.AlterField(
            model_name='orderitemtracker',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
