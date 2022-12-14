# Generated by Django 4.1.1 on 2022-09-07 11:38

from django.db import migrations
import multiselectfield.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('hotel', '0003_alter_hotel_total_rooms_alter_hotel_zipcode'),
    ]

    operations = [
        migrations.AddField(
            model_name='hotel',
            name='amenities',
            field=multiselectfield.db.fields.MultiSelectField(choices=[('bed', 'bed'), ('hot water', 'hot water'), ('wifi', 'wifi'), ('free breakfast', 'free breakfast'), ('coffee', 'coffee'), ('television', 'television'), ('sanitisation', 'sanitisation'), ('medic kit', 'medic kit')], default=1, max_length=50),
            preserve_default=False,
        ),
    ]
