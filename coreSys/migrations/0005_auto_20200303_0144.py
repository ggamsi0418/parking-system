# Generated by Django 3.0.3 on 2020-03-03 01:44

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coreSys', '0004_auto_20200301_2235'),
    ]

    operations = [
        migrations.AlterField(
            model_name='member',
            name='expiration',
            field=models.DateField(default=datetime.datetime(2020, 4, 3, 1, 44, 16, 963508)),
        ),
    ]
