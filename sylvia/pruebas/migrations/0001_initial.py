# Generated by Django 2.2 on 2019-08-15 16:49

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='PreguntaModel',
            fields=[
                ('unico_pregunta', models.AutoField(primary_key=True, serialize=False)),
                ('enunciado', models.TextField()),
                ('alt_a', models.TextField()),
                ('alt_b', models.TextField()),
                ('alt_c', models.TextField()),
                ('alt_d', models.TextField()),
                ('alt_e', models.TextField()),
                ('alt_correcta', models.CharField(max_length=1)),
            ],
        ),
        migrations.CreateModel(
            name='PreguntaPruebaModel',
            fields=[
                ('unico_pregunta_prueba', models.AutoField(primary_key=True, serialize=False)),
                ('p_fija', models.BooleanField()),
                ('p_usar', models.BooleanField()),
                ('pregunta', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pruebas.PreguntaModel')),
                ('usuario', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='TagModel',
            fields=[
                ('id_tag', models.AutoField(primary_key=True, serialize=False)),
                ('tema', models.CharField(max_length=20, null=True)),
                ('usuario', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='PruebaModel',
            fields=[
                ('unico_prueba', models.AutoField(primary_key=True, serialize=False)),
                ('fila', models.TextField(null=True)),
                ('fecha', models.DateTimeField(null=True)),
                ('materia', models.TextField(null=True)),
                ('curso', models.TextField(null=True)),
                ('fecha_timbre', models.DateTimeField(auto_now=True)),
                ('pregunta_prueba', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='pruebas.PreguntaPruebaModel')),
                ('usuario', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='preguntamodel',
            name='tag',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='pruebas.TagModel'),
        ),
        migrations.AddField(
            model_name='preguntamodel',
            name='usuario',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
