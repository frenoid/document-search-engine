# Generated by Django 2.0.4 on 2018-05-30 01:43

import apps.api.models
from django.db import migrations
import djongo.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0011_auto_20180524_0717'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='country',
            name='flag',
        ),
    ]
