# Generated by Django 4.0.3 on 2022-04-01 15:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_countries.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('catalog', '0013_alter_battery_image_alter_bottom_cover_image_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Part',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('model', models.CharField(blank=True, max_length=200, null=True, unique=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('country_id', django_countries.fields.CountryField(max_length=2)),
                ('part_type', models.CharField(blank=True, choices=[('KEYB', 'Keyboard'), ('BOTC', 'Bottom Cover'), ('PALR', 'Palm Rest'), ('LCDC', 'LCD Cover'), ('LCD', 'LCD'), ('CHAR', 'Charger'), ('BATT', 'Battery'), ('CHRP', 'Charging Port'), ('CPUF', 'CPU Fan'), ('LFTH', 'Left Hinge'), ('RGTH', 'Right Hinge'), ('SAT', 'SATA'), ('POR', 'Ports'), ('GRAC', 'Graphics Card'), ('RAM', 'RAM')], max_length=4, null=True)),
                ('image', models.ImageField(blank=True, default='default.png', null=True, upload_to='')),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('laptop_model', models.ManyToManyField(to='catalog.laptop')),
            ],
            options={
                'ordering': ['-updated', '-created'],
            },
        ),
        migrations.RemoveField(
            model_name='bottom_cover',
            name='created_by',
        ),
        migrations.RemoveField(
            model_name='bottom_cover',
            name='laptop_model',
        ),
        migrations.RemoveField(
            model_name='charger',
            name='created_by',
        ),
        migrations.RemoveField(
            model_name='charger',
            name='laptop_model',
        ),
        migrations.RemoveField(
            model_name='charging_port',
            name='created_by',
        ),
        migrations.RemoveField(
            model_name='charging_port',
            name='laptop_model',
        ),
        migrations.RemoveField(
            model_name='cpu_fan',
            name='created_by',
        ),
        migrations.RemoveField(
            model_name='cpu_fan',
            name='laptop_model',
        ),
        migrations.RemoveField(
            model_name='graphics_card',
            name='created_by',
        ),
        migrations.RemoveField(
            model_name='graphics_card',
            name='laptop_model',
        ),
        migrations.RemoveField(
            model_name='keyboard',
            name='created_by',
        ),
        migrations.RemoveField(
            model_name='keyboard',
            name='laptop_model',
        ),
        migrations.RemoveField(
            model_name='lcd',
            name='created_by',
        ),
        migrations.RemoveField(
            model_name='lcd',
            name='laptop_model',
        ),
        migrations.RemoveField(
            model_name='lcd_cover',
            name='created_by',
        ),
        migrations.RemoveField(
            model_name='lcd_cover',
            name='laptop_model',
        ),
        migrations.RemoveField(
            model_name='left_hinge',
            name='created_by',
        ),
        migrations.RemoveField(
            model_name='left_hinge',
            name='laptop_model',
        ),
        migrations.RemoveField(
            model_name='palm_rest',
            name='created_by',
        ),
        migrations.RemoveField(
            model_name='palm_rest',
            name='laptop_model',
        ),
        migrations.RemoveField(
            model_name='ports',
            name='created_by',
        ),
        migrations.RemoveField(
            model_name='ports',
            name='laptop_model',
        ),
        migrations.RemoveField(
            model_name='ram',
            name='created_by',
        ),
        migrations.RemoveField(
            model_name='ram',
            name='laptop_model',
        ),
        migrations.RemoveField(
            model_name='right_hinge',
            name='created_by',
        ),
        migrations.RemoveField(
            model_name='right_hinge',
            name='laptop_model',
        ),
        migrations.RemoveField(
            model_name='sata',
            name='created_by',
        ),
        migrations.RemoveField(
            model_name='sata',
            name='laptop_model',
        ),
        migrations.DeleteModel(
            name='Battery',
        ),
        migrations.DeleteModel(
            name='Bottom_cover',
        ),
        migrations.DeleteModel(
            name='Charger',
        ),
        migrations.DeleteModel(
            name='Charging_Port',
        ),
        migrations.DeleteModel(
            name='CPU_Fan',
        ),
        migrations.DeleteModel(
            name='GRAPHICS_CARD',
        ),
        migrations.DeleteModel(
            name='Keyboard',
        ),
        migrations.DeleteModel(
            name='LCD',
        ),
        migrations.DeleteModel(
            name='LCD_Cover',
        ),
        migrations.DeleteModel(
            name='Left_Hinge',
        ),
        migrations.DeleteModel(
            name='Palm_Rest',
        ),
        migrations.DeleteModel(
            name='PORTS',
        ),
        migrations.DeleteModel(
            name='RAM',
        ),
        migrations.DeleteModel(
            name='Right_Hinge',
        ),
        migrations.DeleteModel(
            name='SATA',
        ),
    ]
