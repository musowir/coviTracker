# Generated by Django 3.1.4 on 2021-03-03 17:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('institutes', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='institute',
            name='location',
            field=models.CharField(max_length=50, null=True),
        ),
    ]
