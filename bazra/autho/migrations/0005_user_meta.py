# Generated by Django 4.2.7 on 2024-04-02 00:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("autho", "0004_alter_user_auth_provider"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="meta",
            field=models.JSONField(blank=True, default=dict, null=True),
        ),
    ]
