# Generated by Django 4.0.6 on 2022-08-01 09:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Token',
        ),
    ]
