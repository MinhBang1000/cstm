# Generated by Django 4.1 on 2022-09-03 13:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='profile_code',
            field=models.CharField(blank=True, default=None, max_length=64, null=True, unique=True),
        ),
    ]
