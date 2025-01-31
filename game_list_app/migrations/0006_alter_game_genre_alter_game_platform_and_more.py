# Generated by Django 5.1.3 on 2024-12-05 08:01

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game_list_app', '0005_platform_add_date_platform_modified_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='genre',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='game',
            name='platform',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='game_list_app.platform'),
        ),
        migrations.AlterField(
            model_name='game',
            name='publisher',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='game_list_app.publisher'),
        ),
        migrations.AlterField(
            model_name='game',
            name='release_date',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
