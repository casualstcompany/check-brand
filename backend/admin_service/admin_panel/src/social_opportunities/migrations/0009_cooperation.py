# Generated by Django 4.1.7 on 2023-12-03 15:22

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):
    dependencies = [
        (
            "social_opportunities",
            "0008_usedservice_status_alter_usedservice_service",
        ),
    ]

    operations = [
        migrations.CreateModel(
            name="Cooperation",
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
                (
                    "email",
                    models.EmailField(
                        max_length=100, unique=True, verbose_name="Почта"
                    ),
                ),
                ("name", models.CharField(max_length=120, verbose_name="Имя")),
                (
                    "phone",
                    models.CharField(max_length=120, verbose_name="Телефон"),
                ),
                (
                    "site",
                    models.CharField(
                        blank=True,
                        max_length=120,
                        null=True,
                        verbose_name="Сайт",
                    ),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[("view", "Просмотрено"), ("new", "Новое")],
                        default="new",
                        max_length=15,
                    ),
                ),
            ],
            options={
                "verbose_name": "Предложения на сотрудничество",
                "verbose_name_plural": "Предложения на сотрудничество",
                "db_table": 'social_opportunities"."cooperation',
            },
        ),
    ]
