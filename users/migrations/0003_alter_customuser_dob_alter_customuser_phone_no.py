# Generated by Django 4.1 on 2024-07-10 04:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_customuser_creater'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='dob',
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='phone_no',
            field=models.CharField(max_length=10, null=True),
        ),
    ]
