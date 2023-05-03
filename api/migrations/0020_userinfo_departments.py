# Generated by Django 4.2 on 2023-04-24 05:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0019_remove_userinfo_department'),
    ]

    operations = [
        migrations.AddField(
            model_name='userinfo',
            name='departments',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='department_involved', to='api.department'),
        ),
    ]
