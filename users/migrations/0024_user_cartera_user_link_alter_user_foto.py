# Generated by Django 4.0.4 on 2022-05-28 01:30

from django.db import migrations, models
import django_resized.forms
import users.models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0023_alter_user_foto'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='cartera',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=19, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='link',
            field=models.CharField(blank=True, max_length=80, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='foto',
            field=django_resized.forms.ResizedImageField(blank=True, crop=None, force_format='JPEG', keep_meta=True, quality=75, size=[500, 500], upload_to=users.models.user_directory_path_profile),
        ),
    ]
