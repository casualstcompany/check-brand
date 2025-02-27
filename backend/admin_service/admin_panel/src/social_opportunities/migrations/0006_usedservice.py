# Generated by Django 4.1.7 on 2023-11-25 20:21

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):
    dependencies = [
        ("nft_tokens", "0008_alter_collection_symbol"),
        (
            "social_opportunities",
            "0005_service_manager_telegram_service_manager_whatsapp",
        ),
    ]

    operations = [
        migrations.CreateModel(
            name="UsedService",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("owner", models.CharField(max_length=255)),
                (
                    "service",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="social_opportunities.service",
                    ),
                ),
                (
                    "token",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="nft_tokens.token",
                    ),
                ),
            ],
            options={
                "verbose_name": "6 - Оказанная услуга",
                "verbose_name_plural": "6 - Оказанные услуги",
                "db_table": 'social_opportunities"."used_service',
            },
        ),
    ]
