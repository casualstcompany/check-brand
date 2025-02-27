# Generated by Django 4.1.7 on 2023-12-01 19:32

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("nft_tokens", "0010_token_email_alter_pack_wallet_owner_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="pack",
            name="price",
            field=models.DecimalField(
                decimal_places=0, max_digits=15, verbose_name="price"
            ),
        ),
        migrations.AlterField(
            model_name="token",
            name="price",
            field=models.DecimalField(
                decimal_places=0, max_digits=15, verbose_name="price"
            ),
        ),
    ]
