# Generated by Django 3.0.3 on 2020-03-06 14:35

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coreSys', '0010_auto_20200306_1411'),
    ]

    operations = [
        migrations.AlterField(
            model_name='member',
            name='expiration',
            field=models.DateField(default=datetime.datetime(2020, 4, 6, 14, 35, 15, 918782)),
        ),
    ]
