# Generated by Django 4.2 on 2023-04-24 09:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0022_userinfo_departments'),
    ]

    operations = [
        migrations.AlterField(
            model_name='document',
            name='project_name',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='documents', to='api.project'),
        ),
    ]