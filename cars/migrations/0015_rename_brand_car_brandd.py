# Generated by Django 4.2.7 on 2023-12-28 23:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cars', '0014_remove_car_acessories_car_acessoriess'),
    ]

    operations = [
        migrations.RenameField(
            model_name='car',
            old_name='brand',
            new_name='brandd',
        ),
    ]
