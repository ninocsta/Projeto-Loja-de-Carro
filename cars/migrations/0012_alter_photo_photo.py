# Generated by Django 4.2.7 on 2023-12-28 22:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cars', '0011_carclientform_mensagem_alter_carclientform_car_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='photo',
            name='photo',
            field=models.ImageField(upload_to='cars/'),
        ),
    ]