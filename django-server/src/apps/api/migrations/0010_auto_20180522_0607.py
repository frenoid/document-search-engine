# Generated by Django 2.0.4 on 2018-05-22 06:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0009_auto_20180518_0831'),
    ]

    operations = [
        migrations.AlterField(
            model_name='countrydetailsbusinessexport',
            name='exported_items_indicator',
            field=models.CharField(blank=True, max_length=75),
        ),
        migrations.AlterField(
            model_name='countrydetailsbusinessexport',
            name='partner_countries_indicator',
            field=models.CharField(blank=True, max_length=75),
        ),
        migrations.AlterField(
            model_name='countrydetailsbusinessfdi',
            name='investor_countries_indicator',
            field=models.CharField(blank=True, max_length=75),
        ),
        migrations.AlterField(
            model_name='countrydetailsbusinessfdi',
            name='net_inflow_indicator',
            field=models.CharField(blank=True, max_length=75),
        ),
        migrations.AlterField(
            model_name='countrydetailsdemographicsage',
            name='distribution_indicator',
            field=models.CharField(blank=True, max_length=75),
        ),
        migrations.AlterField(
            model_name='countrydetailsmobileusage',
            name='distribution_indicator',
            field=models.CharField(blank=True, max_length=75),
        ),
        migrations.AlterField(
            model_name='countrydetailsserviceusage',
            name='distribution_indicator',
            field=models.CharField(blank=True, max_length=75),
        ),
    ]
