# Generated by Django 4.0.4 on 2022-05-29 20:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0024_user_cartera_user_link_alter_user_foto'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='biografia',
            field=models.TextField(blank=True, max_length=200, verbose_name='Bio'),
        ),
    ]
