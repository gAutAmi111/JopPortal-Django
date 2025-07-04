# Generated by Django 5.2.1 on 2025-05-25 07:22

import django.db.models.deletion
import phonenumber_field.modelfields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0004_company_requirements'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='company',
            name='location',
        ),
        migrations.AddField(
            model_name='application',
            name='address',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='jobs.address'),
        ),
        migrations.AddField(
            model_name='company',
            name='address',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='jobs.address'),
        ),
        migrations.AlterField(
            model_name='company',
            name='description',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='company',
            name='website',
            field=models.URLField(max_length=100),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='mobile',
            field=phonenumber_field.modelfields.PhoneNumberField(max_length=128, region=None),
        ),
    ]
