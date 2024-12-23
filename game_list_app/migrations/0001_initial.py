# Generated by Django 5.1.3 on 2024-12-03 12:20

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Publisher',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=254)),
            ],
        ),
        migrations.CreateModel(
            name='Platform',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('release_date', models.DateTimeField(verbose_name='date release')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='game_list_app.publisher')),
            ],
        ),
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('genre', models.CharField(max_length=200)),
                ('release_date', models.DateTimeField(verbose_name='date release')),
                ('platform', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='game_list_app.platform')),
                ('publisher', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='game_list_app.publisher')),
            ],
        ),
        migrations.CreateModel(
            name='Rating',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('grade', models.IntegerField()),
                ('game', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='game_list_app.game')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='game_list_app.user')),
            ],
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=1000)),
                ('rating', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='game_list_app.rating')),
            ],
        ),
    ]
