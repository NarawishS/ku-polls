# Generated by Django 3.1 on 2020-11-01 13:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0005_auto_20201101_2024'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='question',
            name='prev_vote',
        ),
    ]
