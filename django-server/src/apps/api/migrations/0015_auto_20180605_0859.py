# Generated by Django 2.0.4 on 2018-06-05 08:59

import apps.api.models
import core.models
from django.db import migrations
import djongo.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0014_auto_20180605_0615'),
    ]

    operations = [
        migrations.AddField(
            model_name='countrydetailsgeneral',
            name='languages',
            field=djongo.models.fields.ArrayModelField(default=[], model_container=core.models.InfoMeta, model_form_class=apps.api.models.LanguageForm),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='countrydetailsgeneral',
            name='religions',
            field=djongo.models.fields.ArrayModelField(default=[], model_container=core.models.InfoMeta, model_form_class=apps.api.models.ReligionForm),
            preserve_default=False,
        ),
    ]
