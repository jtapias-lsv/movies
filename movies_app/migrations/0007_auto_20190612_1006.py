# Generated by Django 2.2 on 2019-06-12 15:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies_app', '0006_auto_20190612_0958'),
    ]

    operations = [
        migrations.AlterField(
            model_name='actor',
            name='age',
            field=models.PositiveIntegerField(),
        ),
        migrations.AlterField(
            model_name='director',
            name='age',
            field=models.PositiveIntegerField(),
        ),
    ]
