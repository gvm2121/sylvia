
from random import choice,shuffle
from .models import PreguntaModel,AlternativaModel
import pdb
from django.core import serializers


def motor(CANTIDAD_PREGUNTAS,CANTIDAD_FILAS,POOL_DE_PREGUNTAS,PREGUNTAS_FIJAS):
    #pdb.set_trace()
    i=0
    PRUEBA=[]
    CONTENEDOR_PRUEBAS=[]
    while i!=CANTIDAD_FILAS:

        if len(PREGUNTAS_FIJAS)!=0:
            PRUEBA=PREGUNTAS_FIJAS.copy()
            while len(PRUEBA)!=CANTIDAD_PREGUNTAS:
                p=choice(POOL_DE_PREGUNTAS)
                if  p not in PRUEBA:
                    PRUEBA.append(p)
                    
            shuffle(PRUEBA)
            CONTENEDOR_PRUEBAS.append(PRUEBA)
            
            i=i+1

        else:
            PRUEBA=[]
            while len(PRUEBA)!=CANTIDAD_PREGUNTAS:
                #PRUEBA=POOL_DE_PREGUNTAS.copy()
                p=choice(POOL_DE_PREGUNTAS)
                
                if  p not in PRUEBA:
                    PRUEBA.append(p)
                    
            shuffle(PRUEBA)
            CONTENEDOR_PRUEBAS.append(PRUEBA)
            i=i+1
    return CONTENEDOR_PRUEBAS

class PreguntaFinal:
    
    def __init__(self,id_prueba):
        pregunta = PreguntaModel.objects.get(unico_pregunta=id_prueba)
        #ACa hay que intervenir para hacer que aparezca la explicacion
        self.exp = pregunta.explicacion
        self.enunciado = pregunta.enunciado
        #ahora procesamos las alternativas
        abecedario = ['a','b','c','d','e','f']
        self.alternativas = AlternativaModel.objects.filter(enunciado_alternativa=id_prueba).order_by('?') 
        
        zippeado = zip(abecedario,self.alternativas)
        #self.alternativas_de_la_pregunta = AlternativaModel.objects.filter(enunciado_alternativa=id_prueba).order_by('?')
        self.alternativas_de_la_pregunta = zippeado
    def serializado(self):
        dic={}
        alternativas_json = serializers.serialize('json',self.alternativas)
        dic['enunciado']=self.enunciado
        dic['explicacion']=self.exp
        dic['alternativas_json']=alternativas_json
        return dic
        
        
        

    

    
