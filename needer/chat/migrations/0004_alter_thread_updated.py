# Generated by Django 4.0.9 on 2023-02-14 20:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0003_alter_thread_closed_by_first_user_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='thread',
            name='updated',
            field=models.DateTimeField(),
        ),
    ]
