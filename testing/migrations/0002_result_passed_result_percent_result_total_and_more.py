# Generated by Django 5.0.14 on 2025-04-12 16:57

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('testing', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='result',
            name='passed',
            field=models.BooleanField(default=False),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='result',
            name='percent',
            field=models.FloatField(default=0.0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='result',
            name='total',
            field=models.IntegerField(default=False),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='result',
            name='completed_at',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='result',
            name='score',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='result',
            name='test',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='testing.test'),
        ),
        migrations.AlterField(
            model_name='result',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
