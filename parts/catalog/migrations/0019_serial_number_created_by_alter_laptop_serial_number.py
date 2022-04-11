# Generated by Django 4.0.3 on 2022-04-09 14:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('catalog', '0018_alter_part_country_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='serial_number',
            name='created_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='laptop',
            name='serial_number',
            field=models.ManyToManyField(blank=True, to='catalog.serial_number'),
        ),
    ]
