# Generated by Django 4.2.3 on 2023-08-11 20:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mail', '0005_remove_email_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='email',
            name='all_users',
            field=models.BooleanField(blank=True, choices=[(True, 'All USERS'), (False, 'SELECTED USERS')], default=False, null=True),
        ),
    ]
