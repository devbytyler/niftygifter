# Generated by Django 3.2.7 on 2022-11-14 04:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_notification'),
    ]

    operations = [
        migrations.AddField(
            model_name='idea',
            name='price',
            field=models.FloatField(default=0.0),
        ),
    ]
