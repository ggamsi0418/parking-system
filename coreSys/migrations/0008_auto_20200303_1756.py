# Generated by Django 3.0.3 on 2020-03-03 17:56

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coreSys', '0007_auto_20200303_1118'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='pee',
            new_name='fee',
        ),
        migrations.AlterField(
            model_name='member',
            name='expiration',
            field=models.DateField(default=datetime.datetime(2020, 4, 3, 17, 56, 18, 323670)),
        ),
    ]
