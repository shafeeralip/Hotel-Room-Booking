# Generated by Django 3.1.3 on 2020-11-30 13:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admn', '0019_reffreal_offer'),
    ]

    operations = [
        migrations.AddField(
            model_name='reffreal_offer',
            name='offer_type',
            field=models.CharField(max_length=200, null=True),
        ),
    ]