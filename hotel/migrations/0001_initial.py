# Generated by Django 4.1.1 on 2022-09-06 05:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('hotelmanager', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Hotel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('address', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('main_photo', models.ImageField(upload_to='uploads/%Y/%m/%d/')),
                ('photo_2', models.ImageField(blank=True, upload_to='uploads/%Y/%m/%d/')),
                ('photo_3', models.ImageField(blank=True, upload_to='uploads/%Y/%m/%d/')),
                ('photo_4', models.ImageField(blank=True, upload_to='uploads/%Y/%m/%d/')),
                ('total_rooms', models.IntegerField()),
                ('city', models.CharField(max_length=50)),
                ('state', models.CharField(max_length=50)),
                ('available_rooms', models.IntegerField(blank=True, null=True)),
                ('total_rating', models.FloatField(blank=True, null=True)),
                ('customer_visits', models.IntegerField(blank=True, null=True)),
                ('rating_customers', models.IntegerField(blank=True, null=True)),
                ('slug', models.SlugField(max_length=200)),
                ('hotelmanager', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='hotelmanager.hotelmanager')),
            ],
            options={
                'verbose_name': 'Hotel',
                'verbose_name_plural': 'Hotels',
            },
        ),
    ]
