# Generated by Django 2.2 on 2019-06-10 20:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies_app', '0004_auto_20190609_1926'),
    ]

    operations = [
        migrations.AddField(
            model_name='rate',
            name='rate',
            field=models.PositiveIntegerField(default=0),
            preserve_default=False,
        ),
    ]
