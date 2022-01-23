# Generated by Django 2.2.5 on 2021-04-06 08:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('institutes', '0003_auto_20210405_2028'),
    ]

    operations = [
        migrations.AlterField(
            model_name='institute',
            name='staff',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='my_instituite', to='institutes.StaffProfile'),
        ),
        migrations.CreateModel(
            name='VisitedUsers',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('visited_date', models.DateTimeField(auto_now_add=True)),
                ('insitituite', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='institutes.Institute')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
