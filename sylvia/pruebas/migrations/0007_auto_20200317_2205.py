# Generated by Django 2.2 on 2020-03-17 22:05

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pruebas', '0006_auto_20200223_0020'),
    ]

    operations = [
        migrations.AlterField(
            model_name='compartirmodel',
            name='usuario_a_compartir',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='compartirmodel',
            name='yo',
            field=models.IntegerField(),
        ),
    ]
