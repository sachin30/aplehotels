# Generated by Django 4.1.1 on 2022-09-06 06:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('room', '0002_rename_booking_status_room_booked'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='room',
            name='booked',
        ),
        migrations.AddField(
            model_name='room',
            name='booking_status',
            field=models.CharField(choices=[('available', 'available'), ('booked', 'booked')], default=1, max_length=20),
            preserve_default=False,
        ),
    ]
