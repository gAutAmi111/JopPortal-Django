# Generated by Django 5.2.1 on 2025-05-21 15:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0003_alter_application_applicant'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='requirements',
            field=models.TextField(blank=True, help_text='Enter job requirements separated by commas', null=True),
        ),
    ]
