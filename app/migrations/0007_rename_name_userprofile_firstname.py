# Generated by Django 5.0.3 on 2024-05-08 09:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_userprofile_name'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userprofile',
            old_name='name',
            new_name='firstname',
        ),
    ]
