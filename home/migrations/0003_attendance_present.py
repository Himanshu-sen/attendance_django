# Generated by Django 4.1.7 on 2023-04-02 08:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_attendance'),
    ]

    operations = [
        migrations.AddField(
            model_name='attendance',
            name='present',
            field=models.BooleanField(default=False),
        ),
    ]
