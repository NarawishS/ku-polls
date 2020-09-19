# Generated by Django 3.1 on 2020-09-19 07:56

import datetime

from django.db import migrations, models
from django.utils import timezone


class Migration(migrations.Migration):
    dependencies = [
        ('polls', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='end_date',
            field=models.DateTimeField(default=(timezone.now() + timezone.timedelta(days=30)),
                                       verbose_name='closing date'),
            preserve_default=False,
        ),
    ]
