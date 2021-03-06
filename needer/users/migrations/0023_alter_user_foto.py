# Generated by Django 4.0.4 on 2022-05-26 03:07

from django.db import migrations
import django_resized.forms


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0022_alter_user_foto'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='foto',
            field=django_resized.forms.ResizedImageField(blank=True, crop=None, default='default-user.png', force_format='JPEG', keep_meta=True, quality=75, size=[500, 500], upload_to='account/'),
        ),
    ]
