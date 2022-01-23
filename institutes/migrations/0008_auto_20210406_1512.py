# Generated by Django 2.2.5 on 2021-04-06 09:42

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('institutes', '0007_visitedusers_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='visitedusers',
            name='instituite',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='institutes.Institute'),
        ),
        migrations.AlterField(
            model_name='visitedusers',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
