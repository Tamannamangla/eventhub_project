# Generated by Django 5.2 on 2025-04-13 20:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0007_event'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='category',
            field=models.CharField(choices=[('ceremony', 'Ceremony'), ('birthday', 'Birthday'), ('anniversary', 'Anniversary'), ('wedding', 'Wedding'), ('baby-shower', 'Baby Shower')], max_length=50),
        ),
    ]
