# Generated by Django 4.2 on 2023-05-08 14:26

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0009_projectsiteaddress_area_projectsiteaddress_geom_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='owner',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='projects_owned', to=settings.AUTH_USER_MODEL),
        ),
    ]