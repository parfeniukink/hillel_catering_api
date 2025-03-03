# Generated by Django 5.1.5 on 2025-03-03 19:01

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("food", "0003_alter_order_provider"),
    ]

    operations = [
        migrations.AddField(
            model_name="order",
            name="eta",
            field=models.DateField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
