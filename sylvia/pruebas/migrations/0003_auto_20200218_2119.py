# Generated by Django 2.2 on 2020-02-18 21:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pruebas', '0002_compartirmodel'),
    ]

    operations = [
        migrations.RenameField(
            model_name='compartirmodel',
            old_name='tag',
            new_name='tag_a_compartir',
        ),
        migrations.RenameField(
            model_name='compartirmodel',
            old_name='usuario',
            new_name='usuario_a_compartir',
        ),
    ]