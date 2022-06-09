# Generated by Django 4.0.5 on 2022-06-09 01:17

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Cluster',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cluster_name', models.CharField(max_length=50)),
                ('agents_quantity', models.IntegerField(default=0)),
                ('agents_memory', models.IntegerField(default=1)),
                ('date_created', models.DateField()),
                ('is_running', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
            ],
        ),
    ]
