# Generated by Django 4.1 on 2022-09-09 08:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('districts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company_name', models.CharField(max_length=250)),
                ('company_street', models.CharField(max_length=250)),
                ('company_created', models.DateTimeField(auto_now_add=True)),
                ('company_updated', models.DateTimeField(auto_now=True)),
                ('company_district', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='district_companies', to='districts.district')),
            ],
        ),
    ]
