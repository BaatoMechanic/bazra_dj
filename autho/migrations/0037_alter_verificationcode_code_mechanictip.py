# Generated by Django 4.2.7 on 2023-12-13 00:12

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import shortuuidfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('autho', '0036_alter_verificationcode_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='verificationcode',
            name='code',
            field=models.CharField(default=872948, max_length=6),
        ),
        migrations.CreateModel(
            name='MechanicTip',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('idx', shortuuidfield.fields.ShortUUIDField(blank=True, editable=False, max_length=22)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('is_obsolete', models.BooleanField(db_index=True, default=False)),
                ('tip', models.CharField(max_length=500)),
                ('mechanic', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='mechanic_tips', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]