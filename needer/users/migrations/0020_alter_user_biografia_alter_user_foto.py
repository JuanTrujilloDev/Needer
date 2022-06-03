# Generated by Django 4.0.4 on 2022-05-26 03:00

from django.db import migrations, models
import django_resized.forms


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0019_alter_user_foto'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='biografia',
            field=models.TextField(blank=True, max_length=120, verbose_name='Bio'),
        ),
        migrations.AlterField(
            model_name='user',
            name='foto',
            field=django_resized.forms.ResizedImageField(blank=True, crop=None, default='media/account/default.png', force_format='JPEG', keep_meta=True, null=True, quality=75, size=[500, 500], upload_to='account'),
        ),
    ]