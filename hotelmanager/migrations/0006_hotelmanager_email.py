# Generated by Django 4.1.1 on 2022-09-14 11:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hotelmanager', '0005_alter_hotelmanager_manager_phone'),
    ]

    operations = [
        migrations.AddField(
            model_name='hotelmanager',
            name='email',
            field=models.EmailField(default=1, max_length=254),
            preserve_default=False,
        ),
    ]
