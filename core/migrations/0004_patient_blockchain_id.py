# Generated by Django 5.1 on 2024-10-22 16:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_medicalrecord_doctor'),
    ]

    operations = [
        migrations.AddField(
            model_name='patient',
            name='blockchain_id',
            field=models.CharField(blank=True, max_length=66, null=True),
        ),
    ]
