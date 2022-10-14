# Generated by Django 4.0.4 on 2022-06-06 21:09

from django.db import migrations, models
import social.models


class Migration(migrations.Migration):

    dependencies = [
        ('social', '0002_rename_usuario_publicacion_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='publicacion',
            name='titulo',
        ),
        migrations.AlterField(
            model_name='publicacion',
            name='archivo',
            field=models.FileField(blank=True, null=True, upload_to=social.models.postDirectory, validators=[social.models.valid_file_extention]),
        ),
        migrations.AlterField(
            model_name='publicacion',
            name='descripcion',
            field=models.CharField(blank=True, max_length=280, verbose_name='Descripcion'),
        ),
    ]
