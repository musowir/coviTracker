# Generated by Django 3.1.4 on 2021-02-02 19:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('usermanagement', '0002_auto_20210203_0013'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customerprofile',
            name='profile_pic',
        ),
    ]
