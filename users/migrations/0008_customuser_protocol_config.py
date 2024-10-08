# Generated by Django 5.0.6 on 2024-07-07 18:06

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("cluster", "0005_remove_protocalconfig_user"),
        ("users", "0007_delete_dbserver_delete_protocalconfig"),
    ]

    operations = [
        migrations.AddField(
            model_name="customuser",
            name="protocol_config",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="users",
                to="cluster.protocalconfig",
            ),
        ),
    ]
