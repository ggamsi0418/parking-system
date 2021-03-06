# Generated by Django 3.0.3 on 2020-03-03 18:00

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coreSys', '0008_auto_20200303_1756'),
    ]

    operations = [
        migrations.AlterField(
            model_name='member',
            name='expiration',
            field=models.DateField(default=datetime.datetime(2020, 4, 3, 18, 0, 12, 18790)),
        ),
        migrations.AlterField(
            model_name='user',
            name='user_type',
            field=models.NullBooleanField(help_text="'0' is visitor, '1' is member"),
        ),
    ]
