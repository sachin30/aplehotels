# Generated by Django 4.1.1 on 2022-09-28 05:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hotel', '0011_alter_amenity_options'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='hotel',
            name='amenities',
        ),
    ]
