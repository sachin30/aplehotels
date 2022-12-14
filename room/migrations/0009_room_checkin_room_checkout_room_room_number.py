# Generated by Django 4.1.1 on 2022-09-08 09:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('room', '0008_alter_room_hotel'),
    ]

    operations = [
        migrations.AddField(
            model_name='room',
            name='checkin',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='room',
            name='checkout',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='room',
            name='room_number',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]
