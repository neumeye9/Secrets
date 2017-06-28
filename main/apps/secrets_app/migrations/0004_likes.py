# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-06-24 15:39
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('secrets_app', '0003_secrets'),
    ]

    operations = [
        migrations.CreateModel(
            name='Likes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('secret', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='likes', to='secrets_app.Secrets')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='likes', to='secrets_app.Users')),
            ],
        ),
    ]
