# Generated by Django 3.2.9 on 2021-12-07 20:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0003_auto_20211207_2008'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='closed',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
    ]
