# Generated by Django 5.0.6 on 2024-07-19 16:12

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0012_customuser_customer_group"),
    ]

    operations = [
        migrations.AddField(
            model_name="customuser",
            name="note",
            field=models.TextField(blank=True, null=True, verbose_name="Note"),
        ),
    ]
