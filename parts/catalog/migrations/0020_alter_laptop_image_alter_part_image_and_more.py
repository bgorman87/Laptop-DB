# Generated by Django 4.0.3 on 2022-04-15 13:49

import catalog.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0019_serial_number_created_by_alter_laptop_serial_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='laptop',
            name='image',
            field=models.FileField(blank=True, null=True, upload_to='', validators=[catalog.models.validate_file_extension]),
        ),
        migrations.AlterField(
            model_name='part',
            name='image',
            field=models.FileField(blank=True, null=True, upload_to='', validators=[catalog.models.validate_file_extension]),
        ),
        migrations.AlterField(
            model_name='part',
            name='part_type',
            field=models.CharField(blank=True, choices=[('KEYB', 'Keyboard'), ('BOTC', 'Bottom Cover'), ('PALR', 'Palm Rest'), ('LCDC', 'LCD Cover'), ('LCD', 'LCD'), ('LCDB', 'LCD Bezel'), ('LCDT', 'LCD Touch Assembly'), ('TRA', 'Trackpad'), ('SPE', 'Speakers'), ('MIC', 'Microphone'), ('CAM', 'Camera'), ('POW', 'Power Button'), ('HEAT', 'Heatsink'), ('CDD', 'CD Drive'), ('WIFI', 'Wi-Fi Adapter'), ('MOTH', 'Motherboard'), ('WIFA', 'Wi-Fi Antenna'), ('DICA', 'Display Cable'), ('HDDC', 'Hard Drive Caddy'), ('TPFC', 'Trackpad Flex Cable'), ('PBFC', 'Power Button Flex Cable'), ('SB01', 'Sub Board 1'), ('SB02', 'Sub Board 2'), ('SB03', 'Sub Board 3'), ('SBFC', 'Sub Board Flex Cable'), ('CHAR', 'Charger'), ('BATT', 'Battery'), ('CHRP', 'Charging Port'), ('CPUF', 'CPU Fan'), ('LFTH', 'Left Hinge'), ('RGTH', 'Right Hinge'), ('SAT', 'SATA'), ('POR', 'Ports'), ('GRAC', 'Graphics Card'), ('RAM', 'RAM')], max_length=4, null=True),
        ),
    ]