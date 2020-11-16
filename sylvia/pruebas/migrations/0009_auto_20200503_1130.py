# Generated by Django 3.0 on 2020-05-03 11:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pruebas', '0008_auto_20200405_1342'),
    ]

    operations = [
        migrations.CreateModel(
            name='AlternativaModel',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('texto', models.TextField()),
                ('es_correcta', models.BooleanField(default=False)),
                ('dibujo', models.TextField()),
            ],
        ),
        migrations.RemoveField(
            model_name='preguntamodel',
            name='alt_a',
        ),
        migrations.RemoveField(
            model_name='preguntamodel',
            name='alt_b',
        ),
        migrations.RemoveField(
            model_name='preguntamodel',
            name='alt_c',
        ),
        migrations.RemoveField(
            model_name='preguntamodel',
            name='alt_correcta',
        ),
        migrations.RemoveField(
            model_name='preguntamodel',
            name='alt_d',
        ),
        migrations.RemoveField(
            model_name='preguntamodel',
            name='alt_e',
        ),
        migrations.AddField(
            model_name='preguntamodel',
            name='alternativa',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='pruebas.AlternativaModel'),
        ),
    ]
