# Generated by Django 5.2 on 2025-04-13 20:12

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('location', models.CharField(max_length=200)),
                ('time', models.CharField(max_length=100)),
                ('price', models.CharField(max_length=50)),
                ('image', models.ImageField(upload_to='ticket_images/')),
                ('category', models.CharField(choices=[('Music', 'Music')], max_length=100)),
            ],
        ),
    ]
