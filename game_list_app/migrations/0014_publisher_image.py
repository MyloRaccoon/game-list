# Generated by Django 5.1.3 on 2024-12-23 12:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game_list_app', '0013_gamelist_unique_user_game'),
    ]

    operations = [
        migrations.AddField(
            model_name='publisher',
            name='image',
            field=models.ImageField(blank=True, height_field=300, null=True, upload_to='upload', width_field=300),
        ),
    ]
