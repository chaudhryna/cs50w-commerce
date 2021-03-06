# Generated by Django 3.1 on 2020-08-29 16:35

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0019_auto_20200828_2246'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='watchlisted',
            field=models.ManyToManyField(blank=True, default=None, related_name='watchlisted', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='watchlist',
            name='value',
            field=models.CharField(choices=[('Add', 'Add'), ('Remove', 'Remove')], default='Add', max_length=10),
        ),
    ]
