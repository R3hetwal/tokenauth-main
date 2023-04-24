# Generated by Django 4.2 on 2023-04-19 04:41

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('api', '0010_remove_document_additional_docs'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('departments', models.ManyToManyField(related_name='users', to='api.department')),
                ('documents', models.ManyToManyField(related_name='users', to='api.document')),
                ('projects', models.ManyToManyField(related_name='users', to='api.project')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='info', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
