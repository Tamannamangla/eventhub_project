# Generated by Django 5.2 on 2025-04-12 13:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0006_feedback'),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('category', models.CharField(max_length=50)),
                ('location', models.CharField(max_length=100)),
                ('date', models.DateField()),
                ('description', models.TextField()),
                ('image_url', models.URLField(blank=True)),
            ],
        ),
    ]
