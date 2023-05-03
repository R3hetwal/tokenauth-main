# Generated by Django 4.2 on 2023-04-25 13:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0027_userinfo_documents_userinfo_user_profile_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='department',
            name='department_head',
        ),
        migrations.RemoveField(
            model_name='department',
            name='members',
        ),
        migrations.RemoveField(
            model_name='department',
            name='project',
        ),
        migrations.RemoveField(
            model_name='document',
            name='document_owner',
        ),
        migrations.RemoveField(
            model_name='document',
            name='project_name',
        ),
        migrations.RemoveField(
            model_name='project',
            name='owner',
        ),
        migrations.RemoveField(
            model_name='userinfo',
            name='departments',
        ),
        migrations.RemoveField(
            model_name='userinfo',
            name='documents',
        ),
        migrations.RemoveField(
            model_name='userinfo',
            name='projects',
        ),
        migrations.RemoveField(
            model_name='userinfo',
            name='user',
        ),
        migrations.RemoveField(
            model_name='userinfo',
            name='user_profile',
        ),
        migrations.DeleteModel(
            name='AdditionalDoc',
        ),
        migrations.DeleteModel(
            name='Department',
        ),
        migrations.DeleteModel(
            name='Document',
        ),
        migrations.DeleteModel(
            name='Project',
        ),
        migrations.DeleteModel(
            name='UserInfo',
        ),
    ]