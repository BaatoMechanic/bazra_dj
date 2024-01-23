# Generated by Django 4.2.7 on 2023-12-17 09:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('autho', '0051_alter_verificationcode_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userlocation',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='location', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='verificationcode',
            name='code',
            field=models.CharField(default=360609, max_length=6),
        ),
    ]