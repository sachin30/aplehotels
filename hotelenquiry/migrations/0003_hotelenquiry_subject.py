# Generated by Django 4.1.1 on 2022-09-14 09:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hotelenquiry', '0002_alter_hotelenquiry_phone'),
    ]

    operations = [
        migrations.AddField(
            model_name='hotelenquiry',
            name='subject',
            field=models.CharField(default=1, max_length=100),
            preserve_default=False,
        ),
    ]
