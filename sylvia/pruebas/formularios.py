from django.forms import CheckboxInput, ModelForm, Textarea,CharField, TextInput, Select, ValidationError,SelectMultiple,BaseInlineFormSet
from pruebas.models import *
from django import forms
from django.contrib.auth.models import User



class CrearPreguntaForm(ModelForm):
    def __init__(self,*args, **kwargs):
        self.user=kwargs.pop('user')
        super(CrearPreguntaForm, self).__init__(*args, **kwargs)
        self.fields['tag'].queryset = TagModel.objects.filter(usuario=self.user)
    
    class Meta:
        model=PreguntaModel
        exclude=['usuario','alternativa']
        #fields='__all__'
    
        
        widgets = {
            'tag' : SelectMultiple(attrs={'class':'form-control'}),
            'enunciado': Textarea(attrs={'class':'form-control'}),
            'explicacion': Textarea(attrs={'class':'form-control'})            
        }


class CrearPruebaForm(forms.Form):
    nombre_prueba=forms.CharField(label='Nombre de la prueba',max_length=100,widget=forms.TextInput(attrs={'class': 'form-control'}))
    curso =forms.CharField(label='Curso :',max_length=5,widget=forms.TextInput(attrs={'class': 'form-control'})) 
    CantidadPreguntas=forms.IntegerField(label='¿Cuantas preguntas para cada prueba? :',widget=forms.TextInput(attrs={'class': 'form-control'}))
    CantidadFilas =forms.IntegerField(label='¿Cuántas pruebas? :',widget=forms.TextInput(attrs={'class': 'form-control'}))

class CrearTagsForm(ModelForm):
    class Meta:
        model=TagModel
        fields=('tema',)

class FormularioCompartirAux(forms.Form):
    usuario_a_compartir = forms.IntegerField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    tag_a_compartir = forms.IntegerField()

class FormularioCompartir(ModelForm):
    def __init__(self,*args, **kwargs):
        self.usuario=kwargs.pop('usuario')
        super(FormularioCompartir, self).__init__(*args, **kwargs)
        self.fields['tag_a_compartir'].queryset = TagModel.objects.filter(usuario=self.usuario)
     
    class Meta:
        model=CompartirModel
        #exclude=['yo',]
        fields=['usuario_a_compartir','tag_a_compartir']
        widgets = {
            'usuario_a_compartir': TextInput(attrs={'class':'form-control'}),
             'tag_a_compartir': Select(attrs={'class':'form-control'})
            
        }
        #el usuario_a_compartir debe se Textarea para que pueda trabajar con jquery

class AlternativaForm(ModelForm):
    class Meta:
        model=AlternativaModel
        fields=['texto','es_correcta']
        widgets = {
            'texto': Textarea(attrs={'class':'form-control'}),
            'es_correcta': CheckboxInput(attrs={'class':'form-control'})            
        }
 

class EnunciadoForm(ModelForm):
    #Este solo se usa en la vista para editar las preguntas
    class Meta:
        model=PreguntaModel
        fields=['enunciado','explicacion']

from django.forms import BaseFormSet

class PreguntaCompletaFormset(BaseFormSet):
    def clean(self):
        es_correcta_list = []
        for f in self.forms:
            es_correcta = f.cleaned_data.get("es_correcta")
            es_correcta_list.append(es_correcta)
        if sum(es_correcta_list)==0: #suma los true, que valen 1, si no hay true no se marcó la alternativa correcta
            raise ValidationError("Falta marcar la alternativa correcta")
        if sum(es_correcta_list)>1: #si la suma es mayor a 1, hay mas alternativas marcadas
            raise ValidationError("Hay que marcar solo 1 alternativa como correcta, hay más de una marcada. Ojo.")
                    

class PreguntaCompletaFormsetEditada(BaseInlineFormSet):
    def clean(self):
        print(self.forms)
        es_correcta_list = []
        for f in self.forms:
            es_correcta = f.cleaned_data.get("es_correcta")
            es_correcta_list.append(es_correcta)
        if sum(es_correcta_list)==0: #suma los true, que valen 1, si no hay true no se marcó la alternativa correcta
            raise ValidationError("Falta marcar la alternativa correcta")
        if sum(es_correcta_list)>1: #si la suma es mayor a 1, hay mas alternativas marcadas
            raise ValidationError("Hay que marcar solo 1 alternativa como correcta, hay más de una marcada. Ojo.")
        




#aca hay que 
#pensar en una lógica de formulario para compartir las tags entre profesores y colegios
