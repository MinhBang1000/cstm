# Generated by Django 4.1 on 2022-11-08 04:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pallets', '0002_pallet_pallet_color'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pallet',
            name='pallet_x',
        ),
        migrations.RemoveField(
            model_name='pallet',
            name='pallet_y',
        ),
        migrations.RemoveField(
            model_name='pallet',
            name='pallet_z',
        ),
        migrations.AddField(
            model_name='pallet',
            name='pallet_active',
            field=models.BooleanField(default=False),
        ),
    ]