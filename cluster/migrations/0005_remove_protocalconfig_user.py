# Generated by Django 5.0.6 on 2024-07-07 17:34

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("cluster", "0004_protocalconfig_user"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="protocalconfig",
            name="user",
        ),
    ]
