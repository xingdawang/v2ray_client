# Generated by Django 5.0.6 on 2024-07-11 19:57

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        (
            "IP_resource",
            "0002_remove_ipresource_description_ipresource_expire_date_and_more",
        ),
        ("cluster", "0006_alter_protocalconfig_expiry_time_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="ipresource",
            name="db_server",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="users",
                to="cluster.dbserver",
            ),
        ),
    ]
