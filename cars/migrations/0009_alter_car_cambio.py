# Generated by Django 4.2.7 on 2023-12-11 23:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cars', '0008_alter_car_factory_year_alter_car_model_year'),
    ]

    operations = [
        migrations.AlterField(
            model_name='car',
            name='cambio',
            field=models.CharField(choices=[('Automático', 'Automático'), ('Manual', 'Manual')], default='Manual', max_length=20),
        ),
    ]