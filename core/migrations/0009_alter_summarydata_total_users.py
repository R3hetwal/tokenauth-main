# Generated by Django 4.2 on 2023-04-28 10:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_alter_summarydata_total_projects'),
    ]

    operations = [
        migrations.AlterField(
            model_name='summarydata',
            name='total_users',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]