# Generated by Django 3.1 on 2020-08-25 17:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0014_listing_picture'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='picture',
            field=models.ImageField(blank=True, null=True, upload_to='images'),
        ),
    ]
