# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PersonalInfo',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('email_addr', models.CharField(max_length=60)),
                ('password', models.CharField(max_length=20)),
                ('user_name', models.CharField(max_length=40)),
                ('status', models.BooleanField(default=False)),
                ('token', models.CharField(max_length=256)),
                ('time', models.DateTimeField(verbose_name='Login time')),
            ],
        ),
        migrations.CreateModel(
            name='PersonalProject',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('project_name', models.CharField(max_length=40)),
                ('person', models.ForeignKey(to='db_manager.PersonalInfo')),
            ],
        ),
        migrations.CreateModel(
            name='ProjectInfo',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('email_addr', models.CharField(max_length=60)),
                ('user_name', models.CharField(max_length=40)),
                ('project_name', models.CharField(max_length=50)),
                ('project_status', models.BooleanField(default=False)),
            ],
        ),
    ]
