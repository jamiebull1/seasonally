# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-04-21 15:06
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_auto_20170421_1652'),
    ]

    operations = [
        migrations.CreateModel(
            name='Month',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=9)),
                ('num', models.IntegerField()),
            ],
        ),
        migrations.RemoveField(
            model_name='product',
            name='apr',
        ),
        migrations.RemoveField(
            model_name='product',
            name='aug',
        ),
        migrations.RemoveField(
            model_name='product',
            name='dec',
        ),
        migrations.RemoveField(
            model_name='product',
            name='feb',
        ),
        migrations.RemoveField(
            model_name='product',
            name='jan',
        ),
        migrations.RemoveField(
            model_name='product',
            name='jul',
        ),
        migrations.RemoveField(
            model_name='product',
            name='jun',
        ),
        migrations.RemoveField(
            model_name='product',
            name='mar',
        ),
        migrations.RemoveField(
            model_name='product',
            name='may',
        ),
        migrations.RemoveField(
            model_name='product',
            name='nov',
        ),
        migrations.RemoveField(
            model_name='product',
            name='oct',
        ),
        migrations.RemoveField(
            model_name='product',
            name='sep',
        ),
        migrations.AddField(
            model_name='product',
            name='months',
            field=models.ManyToManyField(to='api.Month'),
        ),
    ]
