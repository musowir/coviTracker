# Generated by Django 2.2.5 on 2021-04-07 05:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('institutes', '0008_auto_20210406_1512'),
    ]

    operations = [
        migrations.AddField(
            model_name='institute',
            name='is_verfilfied',
            field=models.BooleanField(default=False),
        ),
    ]
