# Generated by Django 4.0.4 on 2022-05-23 17:18

from django.db import migrations, models
import django_resized.forms


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_alter_pais_options_alter_pais_nombre'),
    ]

    operations = [
        migrations.CreateModel(
            name='TipoCelebridad',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=24, verbose_name='Nombre')),
            ],
            options={
                'verbose_name': 'Tipo Celebridad',
                'verbose_name_plural': 'Tipos de Celebridad',
                'ordering': ['nombre'],
            },
        ),
        migrations.AddField(
            model_name='user',
            name='biografia',
            field=models.TextField(blank=True, max_length=120, verbose_name='Bio'),
        ),
        migrations.AddField(
            model_name='user',
            name='fecha_nacimiento',
            field=models.DateField(blank=True, null=True, verbose_name='Fecha nacimiento'),
        ),
        migrations.AddField(
            model_name='user',
            name='foto',
            field=django_resized.forms.ResizedImageField(blank=True, crop=None, force_format=None, keep_meta=True, quality=0, size=[500, 500], upload_to='media/account'),
        ),
        migrations.AddField(
            model_name='user',
            name='genero',
            field=models.CharField(choices=[('Hombre', 'Hombre'), ('Mujer', 'Mujer'), ('Otro', 'Otro')], default='Otro', max_length=7),
        ),
        migrations.AddField(
            model_name='user',
            name='slug',
            field=models.SlugField(null=True, verbose_name='Slug'),
        ),
        migrations.AddField(
            model_name='user',
            name='tipo_celebridad',
            field=models.ManyToManyField(blank=True, to='users.tipocelebridad'),
        ),
    ]
