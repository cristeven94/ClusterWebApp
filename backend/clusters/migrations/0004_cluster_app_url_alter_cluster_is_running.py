# Generated by Django 4.0.5 on 2022-09-29 03:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clusters', '0003_alter_cluster_user_alter_node_ram_usage'),
    ]

    operations = [
        migrations.AddField(
            model_name='cluster',
            name='app_url',
            field=models.CharField(default='', max_length=200),
        ),
        migrations.AlterField(
            model_name='cluster',
            name='is_running',
            field=models.BooleanField(default=True),
        ),
    ]
