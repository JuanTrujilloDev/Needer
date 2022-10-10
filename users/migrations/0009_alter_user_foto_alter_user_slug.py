# Generated by Django 4.0.4 on 2022-05-23 18:00

from django.db import migrations, models
import django_resized.forms


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0008_tipocelebridad_user_biografia_user_fecha_nacimiento_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='foto',
            field=django_resized.forms.ResizedImageField(blank=True, crop=None, default='account/default.png', force_format=None, keep_meta=True, quality=0, size=[500, 500], upload_to='media/account'),
        ),
        migrations.AlterField(
            model_name='user',
            name='slug',
            field=models.SlugField(blank=True, null=True, verbose_name='Slug'),
        ),
    ]
