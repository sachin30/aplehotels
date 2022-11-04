# Generated by Django 4.1.1 on 2022-09-06 05:38

from django.db import migrations, models
import hotelmanager.models


class Migration(migrations.Migration):

    dependencies = [
        ('hotelmanager', '0002_alter_hotelmanager_manager_phone'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hotelmanager',
            name='manager_phone',
            field=models.CharField(max_length=10, validators=[hotelmanager.models.valid_phonenumber]),
        ),
    ]
