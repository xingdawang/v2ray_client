# Generated by Django 5.0.6 on 2024-07-19 15:49

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        (
            "cluster",
            "0008_alter_dbserver_options_alter_protocalconfig_options_and_more",
        ),
    ]

    operations = [
        migrations.AlterField(
            model_name="dbserver",
            name="pem_name",
            field=models.CharField(max_length=100, verbose_name="pem name"),
        ),
    ]
