# Generated by Django 2.2 on 2019-06-10 00:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies_app', '0002_auto_20190609_1909'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movie',
            name='duration',
            field=models.PositiveIntegerField(),
        ),
    ]
