# Generated by Django 4.0.4 on 2022-05-31 21:07

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import social.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Publicacion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(max_length=250, verbose_name='Titulo')),
                ('descripcion', models.CharField(blank=True, max_length=150, verbose_name='Descripcion')),
                ('archivo', models.FileField(blank=True, null=True, upload_to=social.models.postDirectory)),
                ('fecha_creacion', models.DateTimeField(auto_now_add=True, verbose_name='Fecha Publicacion')),
                ('fecha_actualizacion', models.DateTimeField(auto_now_add=True, verbose_name='Fecha Actualizacion')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Autor')),
            ],
        ),
    ]