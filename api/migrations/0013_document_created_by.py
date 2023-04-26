# Generated by Django 4.2 on 2023-04-19 06:50

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('api', '0012_alter_userinfo_departments_alter_userinfo_documents_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='document',
            name='created_by',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]