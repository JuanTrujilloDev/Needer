# Generated by Django 4.0.4 on 2022-05-13 20:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_remove_user_group_remove_user_groups_user_groups'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='tipo_documento',
        ),
        migrations.AddField(
            model_name='user',
            name='pais',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='Pais'),
        ),
    ]
