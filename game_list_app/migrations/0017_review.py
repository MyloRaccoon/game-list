# Generated by Django 5.1.5 on 2025-02-04 09:12

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game_list_app', '0016_alter_gamelist_state'),
    ]

    operations = [
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rate', models.CharField(choices=[('1/5', 'One'), ('2/5', 'Two'), ('3/5', 'Trhee'), ('4/5', 'Four'), ('5/5', 'Five')], default='5/5', max_length=10)),
                ('review', models.TextField(blank=True, null=True)),
                ('game_list', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='game_list_app.gamelist')),
            ],
        ),
    ]
