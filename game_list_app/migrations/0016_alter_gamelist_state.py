# Generated by Django 5.1.3 on 2025-01-06 14:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game_list_app', '0015_game_image_platform_image_alter_publisher_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gamelist',
            name='state',
            field=models.CharField(choices=[('want', 'Want to play'), ('playing', 'Playing'), ('finished', 'Finished'), ('hundred', '100%'), ('dropped', 'Dropped')], default='playing', max_length=10),
        ),
    ]
