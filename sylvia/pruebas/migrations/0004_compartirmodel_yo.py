# Generated by Django 2.2 on 2020-02-22 20:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pruebas', '0003_auto_20200218_2119'),
    ]

    operations = [
        migrations.AddField(
            model_name='compartirmodel',
            name='yo',
            field=models.TextField(default='-'),
        ),
    ]
