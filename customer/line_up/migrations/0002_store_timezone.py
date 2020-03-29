# Generated by Django 2.2.11 on 2020-03-29 02:38

from django.db import migrations
import timezone_field.fields


class Migration(migrations.Migration):

    dependencies = [
        ('line_up', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='store',
            name='timezone',
            field=timezone_field.fields.TimeZoneField(default=None),
            preserve_default=False,
        ),
    ]
