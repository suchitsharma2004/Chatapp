# Generated by Django 5.0.7 on 2024-07-10 15:46

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("chat", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="draft",
            name="date_saved",
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]