# Generated by Django 4.0.3 on 2022-04-11 01:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.DeleteModel(
            name='ActiveResetShaKeys',
        ),
    ]
