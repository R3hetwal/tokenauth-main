# Generated by Django 4.2 on 2023-05-08 08:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_projectsite'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='projectsiteaddress',
            name='geom_type',
        ),
    ]
