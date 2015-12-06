# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('db_manager', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='personalproject',
            old_name='person',
            new_name='personalinfo',
        ),
    ]
