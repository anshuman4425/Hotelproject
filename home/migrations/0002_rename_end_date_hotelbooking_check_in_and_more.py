# Generated by Django 5.0.6 on 2024-07-13 00:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='hotelbooking',
            old_name='end_date',
            new_name='check_in',
        ),
        migrations.RenameField(
            model_name='hotelbooking',
            old_name='start_date',
            new_name='check_out',
        ),
    ]
