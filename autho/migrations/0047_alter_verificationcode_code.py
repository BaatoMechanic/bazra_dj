# Generated by Django 4.2.7 on 2023-12-16 10:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('autho', '0046_alter_verificationcode_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='verificationcode',
            name='code',
            field=models.CharField(default=514861, max_length=6),
        ),
    ]
