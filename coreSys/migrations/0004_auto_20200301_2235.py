# Generated by Django 3.0.3 on 2020-03-01 22:35

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coreSys', '0003_auto_20200229_1353'),
    ]

    operations = [
        migrations.AlterField(
            model_name='member',
            name='expiration',
            field=models.DateField(default=datetime.datetime(2020, 4, 1, 22, 35, 39, 131812)),
        ),
    ]
