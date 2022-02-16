from django.db import models
from registro.models import *
from django.contrib.auth.models import User
from random import shuffle

class TagModel(models.Model):
    id_tag=models.AutoField(primary_key=True)
    usuario=models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    tema=models.CharField(null=True, max_length=20)
    def todos(self,request):
        todo=self.Objects.filter(usuario=request.user)
        return todo
    def __str__(self):
        return self.tema

#este model crea la pregunta que puede ser utilizada en cualquier parte



class PreguntaModel(models.Model):
    usuario=models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    tag=models.ManyToManyField(TagModel)
    unico_pregunta=models.AutoField(primary_key=True)
    enunciado = models.TextField()
    explicacion = models.TextField(null=True)
    
    
    def todos(self,request):
        todo=self.objects.filter(usuario=request.user)
        return todo
    def __str__(self):
        return self.enunciado

class AlternativaModel(models.Model):
    id_alternativa = models.AutoField(primary_key=True)
    texto = models.TextField()
    es_correcta = models.BooleanField(default=False)
    dibujo = models.TextField(null=True)
    enunciado_alternativa = models.ForeignKey(PreguntaModel,on_delete=models.CASCADE,null=True)

    
#Este especifica el comportamiento de la pregunta dentro de la prueba.
#si será pregunta fija, si será única, etc.
class PreguntaPruebaModel(models.Model):
    usuario=models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    unico_pregunta_prueba=models.AutoField(primary_key=True)
    pregunta=models.ForeignKey(PreguntaModel,on_delete=models.CASCADE)
    p_fija=models.BooleanField()
    p_usar=models.BooleanField()

#Este model crea la prueba en genera, la engloba.
class PruebaModel(models.Model):
    usuario=models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    unico_prueba=models.AutoField(primary_key=True)
    pregunta_prueba=models.ForeignKey(PreguntaPruebaModel,on_delete=models.CASCADE,null=True)
    fila=models.TextField(null=True)
    fecha=models.DateTimeField(null=True)
    materia=models.TextField(null=True)
    curso=models.TextField(null=True)
    fecha_timbre=models.DateTimeField(auto_now=True,null=False)


class CompartirModel(models.Model):
    numero_compartido = models.AutoField(primary_key=True)
    yo = models.IntegerField(null=True)
    usuario_a_compartir = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    tag_a_compartir = models.ForeignKey(TagModel,on_delete=models.CASCADE,null=True)




#acá debería ir despues: materias, profesores y colegios.