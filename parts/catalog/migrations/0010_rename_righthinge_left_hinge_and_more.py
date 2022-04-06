# Generated by Django 4.0.3 on 2022-03-29 10:39

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('catalog', '0009_lefthinge_righthinge_delete_hinges'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='RightHinge',
            new_name='Left_Hinge',
        ),
        migrations.RenameModel(
            old_name='LeftHinge',
            new_name='Right_Hinge',
        ),
        migrations.RenameField(
            model_name='left_hinge',
            old_name='right_hinge_model',
            new_name='left_hinge_model',
        ),
        migrations.RenameField(
            model_name='right_hinge',
            old_name='left_hinge_model',
            new_name='right_hinge_model',
        ),
    ]
