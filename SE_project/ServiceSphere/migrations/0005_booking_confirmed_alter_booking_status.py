# Generated by Django 5.0.4 on 2024-04-17 19:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ServiceSphere', '0004_rename_date_booking_date_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking',
            name='confirmed',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='booking',
            name='status',
            field=models.BooleanField(default=False),
        ),
    ]
