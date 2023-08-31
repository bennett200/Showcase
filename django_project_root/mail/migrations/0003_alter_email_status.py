# Generated by Django 4.2.3 on 2023-08-11 06:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mail', '0002_remove_email_current_email_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='email',
            name='status',
            field=models.BooleanField(blank=True, choices=[(True, 'Active'), (False, 'Unactive')], default=False, null=True, unique=True),
        ),
    ]
