# Generated by Django 4.0.4 on 2022-06-11 15:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0028_remove_user_groups_user_groups'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='verificado',
            field=models.BooleanField(default=False, verbose_name='verificado'),
        ),
    ]