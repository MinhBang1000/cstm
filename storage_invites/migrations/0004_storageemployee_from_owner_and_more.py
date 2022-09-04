# Generated by Django 4.1 on 2022-09-04 07:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('storage_invites', '0003_rename_to_role_storageemployee_for_role'),
    ]

    operations = [
        migrations.AddField(
            model_name='storageemployee',
            name='from_owner',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='storageemployee',
            name='for_role',
            field=models.CharField(blank=True, default='Supervisor', max_length=50, null=True),
        ),
    ]
