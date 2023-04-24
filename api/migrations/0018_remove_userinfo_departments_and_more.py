# Generated by Django 4.2 on 2023-04-24 04:48

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('api', '0017_remove_document_created_by'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userinfo',
            name='departments',
        ),
        migrations.RemoveField(
            model_name='userinfo',
            name='documents',
        ),
        migrations.AddField(
            model_name='userinfo',
            name='department',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='api.department'),
        ),
        migrations.AlterField(
            model_name='userinfo',
            name='projects',
            field=models.ManyToManyField(to='api.project'),
        ),
        migrations.AlterField(
            model_name='userinfo',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
