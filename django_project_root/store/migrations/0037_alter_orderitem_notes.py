# Generated by Django 4.2.3 on 2023-08-07 02:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0036_alter_orderitem_notes'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderitem',
            name='notes',
            field=models.TextField(blank=True, default='No Notes', max_length=150, null=True),
        ),
    ]
