# Generated by Django 4.1.7 on 2023-03-11 11:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0005_remove_auction_place_bids_auction_place_bids'),
    ]

    operations = [
        migrations.RenameField(
            model_name='auction',
            old_name='place_bids',
            new_name='place_bid',
        ),
    ]
