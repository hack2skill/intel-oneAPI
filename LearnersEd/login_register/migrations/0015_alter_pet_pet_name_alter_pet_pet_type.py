# Generated by Django 4.1.9 on 2023-06-25 19:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login_register', '0014_pet_delete_virtualpet'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pet',
            name='pet_name',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AlterField(
            model_name='pet',
            name='pet_type',
            field=models.CharField(default='', max_length=100),
        ),
    ]
