from django.forms import modelformset_factory,formset_factory,inlineformset_factory
from django.shortcuts import render,redirect
from django.http import HttpResponse,JsonResponse,FileResponse
from .models import PreguntaModel,PruebaModel,AlternativaModel
from pruebas.formularios import *
from django.contrib.auth.models import User
from django.core import serializers
from .funciones_externas import motor,PreguntaFinal
import json
import os

def index(request):
    usuario=request.user
    print('Dentro del index',usuario)
    return render(request,'pruebas/index.html',{'usuario':usuario})



def crear_pregunta(request):
    context={}
    AlternativasFormSet = formset_factory(AlternativaForm,extra=5, formset=PreguntaCompletaFormset) #el PreguntaCompletaFormset es para validar el formulario
    context['crear_pregunta_formulario']=CrearPreguntaForm(user=request.user) #Crea el encabezado
    context['formulario_alternativas'] = AlternativasFormSet() #Crea un paquete de 5 preguntas
    
    return render(request,'pruebas/crear_pregunta.html',context)

def crear_pregunta_procesar(request):
    context={}
    if request.method == 'POST':
        form = CrearPreguntaForm(request.POST,user=request.user) #creamos el enunciado
        AlternativasFormSet = formset_factory(AlternativaForm,extra=5,formset=PreguntaCompletaFormset) #crea un paquete de 5 formularios tipo alternativa
        formularioAlternativa = AlternativasFormSet(request.POST or None)
        if form.is_valid() and formularioAlternativa.is_valid():
            #pregunta_enunciado = form.cleaned_data['enunciado']
            pregunta_tag = form.cleaned_data['tag']
            fs = form.save(commit=False)
            fs.usuario=request.user
            fs.save()
            fs.tag.set(pregunta_tag) #método set para asignar manytomany, debemos antes guardar el formulario
            
            for f in formularioAlternativa:
                alternativa_texto = f.cleaned_data['texto']
                alternativa_correcta = f.cleaned_data['es_correcta']
                Alternativa = AlternativaModel(
                    texto = alternativa_texto,
                    es_correcta = alternativa_correcta,
                    enunciado_alternativa = fs
                    )
                Alternativa.save()
            return redirect('crear_pregunta')
        else:
            #mandamos los formularios devuelta a la vista con los errores en él
            context['formulario_alternativas'] = formularioAlternativa
            context['crear_pregunta_formulario']=form
            return render(request,'pruebas/crear_pregunta.html',context)

    return render(request,'pruebas/crear_pregunta.html',context)



def crear_prueba(request):
    data = {}
    data['crear_prueba_formulario'] = CrearPruebaForm()
    tag_compartidos = CompartirModel.objects.filter(usuario_a_compartir = request.user).values_list('tag_a_compartir') or None
    data['preguntas'] = PreguntaModel.objects.filter(usuario=request.user).order_by('unico_pregunta')
    if tag_compartidos:
        preguntas_compartidas = PreguntaModel.objects.filter(tag__in = tag_compartidos)
        data['preguntas_compartidas'] = preguntas_compartidas
    
    return render(request,'pruebas/crear-prueba.html',data)


def preguntas_guardadas(request):
    data = {}
    tag_compartidos = CompartirModel.objects.filter(usuario_a_compartir = request.user).values_list('tag_a_compartir') or None
    preguntas = PreguntaModel.objects.filter(usuario=request.user).order_by('unico_pregunta')
    data['preguntas'] = preguntas
    if tag_compartidos:
        preguntas_compartidas = PreguntaModel.objects.filter(tag__in = tag_compartidos)
        data['preguntas_compartidas'] = preguntas_compartidas
    return render(request,'pruebas/preguntas-guardadas.html',data)

def salir(request):
    request.session.flush()
    return redirect('login_inicial')

def crear_tags(request):
    crear_tags_formulario=CrearTagsForm()
    #vemos las etiquetas creadas
    etiquetas=TagModel.objects.filter(usuario=request.user)
    etiquetas_externas=CompartirModel.objects.filter(usuario_a_compartir=request.user.id)
    return render(request,'pruebas/tags.html',{'crear_tags_formulario':crear_tags_formulario,'etiquetas':etiquetas,'etiquetas_externas':etiquetas_externas})

def guardar_tags(request):
    context={}
    if request.method == 'POST':
       
        form = CrearTagsForm(request.POST)
        if form.is_valid():
            fs=form.save(commit=False)
            tema = form.cleaned_data['tema']
            fs.tema=tema
            fs.usuario=request.user
            fs.save()
            return redirect('crear_tag')

    # if a GET (or any other method) we'll create a blank form
        else:
            print('Hay un error en el formulario')
            return redirect('crear_tags')

    return render(request,'pruebas/crear_pregunta.html',context) 

def procesar(request):
    if request.method == 'POST':
        algo=request.POST.copy()
    return HttpResponse('procesar')


def preguntas_guardadas_procesar(request):
    if request.method == 'POST':
        preguntas_edit=request.POST.copy()
        if preguntas_edit['accion']=='Borrar':
            pregunta_borrar=PreguntaModel.objects.get(usuario=request.user,unico_pregunta=preguntas_edit['pregunta_numero'])
            pregunta_borrar.delete()
            return redirect('preguntas_guardadas')
        

def preguntas_editadas(request,unico_pregunta):
    context={}
    context['unico_pregunta']=unico_pregunta
    FormularioAlternativa = inlineformset_factory(
        PreguntaModel,
        AlternativaModel,
        fields=('texto','es_correcta','enunciado_alternativa'), 
        extra=0,
        can_delete=False
    )
    enunciado = PreguntaModel.objects.get(unico_pregunta=unico_pregunta,usuario=request.user)
    tags = PreguntaModel.objects.filter(unico_pregunta=unico_pregunta).values('tag')
    context['editar_enunciado_formulario']=CrearPreguntaForm(
        instance=enunciado,
        user=request.user,
        # initial={
        #     'tag':tags
        # }
        )
    context['editar_formulario_alternativas'] = FormularioAlternativa(instance=enunciado)
    
    return render(request,'pruebas/editar_pregunta.html',context)

def guardar_pregunta_editada(request):
    copia=request.POST.copy()
    tags = request.POST.getlist("tag")
    enunciado = PreguntaModel.objects.get(unico_pregunta=copia['unico'])
    
    if request.method=="POST" and copia['accion']=='Actualizar':
        FormularioAlternativaClass = inlineformset_factory(
            PreguntaModel,
            AlternativaModel,
            fields=('texto','es_correcta'),
            extra=0,
            can_delete = False,
            formset=PreguntaCompletaFormsetEditada
            )
        Enunciado_desde_form = EnunciadoForm(request.POST, instance=enunciado)
        #Enunciado_desde_form = EnunciadoForm(request.POST)
        formularioAlternativa = FormularioAlternativaClass(request.POST,instance=enunciado)
        #formularioAlternativa = FormularioAlternativaClass(request.POST)
        if Enunciado_desde_form.is_valid() and formularioAlternativa.is_valid():
            Enunciado_desde_form.save()
            formularioAlternativa.save()
        else:
            context={}
            FormularioAlternativa = inlineformset_factory(PreguntaModel,AlternativaModel,fields=('texto','es_correcta','enunciado_alternativa'), extra=0,can_delete=False)
            context['editar_formulario_alternativas'] = FormularioAlternativa(instance=enunciado)
            context['editar_enunciado_formulario']=EnunciadoForm(instance=enunciado)
            return render(request,'pruebas/editar_pregunta.html',context)
    return redirect('preguntas_guardadas')


def generar_prueba(request):
    encabezado_jason={}
    configuracion_prueba=request.POST.copy()
    preguntas_seleccionadas=[]
    preguntas_fijas=[]
    cantidad_filas=int(configuracion_prueba['CantidadFilas'])
    cantidad_preguntas=int(configuracion_prueba['CantidadPreguntas'])
    encabezado_jason['curso']=configuracion_prueba['curso']
    encabezado_jason['nombre_prueba']=configuracion_prueba['nombre_prueba']
    for k,v in configuracion_prueba.items():
        if v=='on' and k.isdigit():
            preguntas_seleccionadas.append(k)
        if v=='on' and k.startswith('fija_'):
            fija=k.strip('fija_')
            preguntas_fijas.append(fija)
    contenedor=motor(
        POOL_DE_PREGUNTAS=preguntas_seleccionadas,
    CANTIDAD_FILAS=cantidad_filas,
    PREGUNTAS_FIJAS=preguntas_fijas,
    CANTIDAD_PREGUNTAS=cantidad_preguntas
    )
    contenedor_final=[]
    enumeracion_preguntas = [n for n in range(1,cantidad_preguntas+1)]
    pruebas = {}
    m = 0
    for i in contenedor:
        contenedor_auxiliar = [] # Preview
        contenedor_json=[] # Latex
        m = m+1 #latex
        for j in i:
            p = PreguntaFinal(id_prueba=j)
            contenedor_json.append(p.serializado()) # Latex
            contenedor_auxiliar.append(p) # Preview
            contenedor_auxiliar_2=zip(enumeracion_preguntas,contenedor_auxiliar) # Preview
        pruebas[str(m)]=contenedor_json # Latex
        contenedor_final.append(contenedor_auxiliar_2) # Preview
    pruebas['encabezado'] = encabezado_jason
    pruebas['cantidad_preguntas']=cantidad_preguntas
    request.session['contenedor']=pruebas
    
    return render(request,'pruebas/preview-prueba.html',{'contenedor_final':contenedor_final})


def generar_pdf(request):
    prueba = request.session.get('contenedor')
    cantidad_preguntas=prueba['cantidad_preguntas']
    archivo_salida = open("prueba.tex","w")
    archivo_salida.write("\\documentclass[10pt,oneside,letterpaper]{article}")
    archivo_salida.write("\\usepackage[utf8x]{inputenc}")
    archivo_salida.write("\\usepackage{enumitem}")
    #archivo_salida.write("\\usepackage{fancyhrd}")
    archivo_salida.write("\\usepackage{tikz}")
    archivo_salida.write("\\usepackage[T1]{fontenc}")
    archivo_salida.write("\\usepackage{lipsum}")
    archivo_salida.write("\\usepackage{pgfplots}")
    archivo_salida.write("\\usepgflibrary{shapes.geometric}")
    archivo_salida.write("\\usetikzlibrary{calc}")
    archivo_salida.write("\\usepackage[margin=3cm]{geometry}")
    archivo_salida.write("\\usepackage{multicol}")
    

    archivo_salida.write("\\newcommand*\\circled[1]{\\tikz[baseline=(char.base)]{\\node[shape=circle,draw,inner sep=1.2pt] (char) {#1};}}")
    archivo_salida.write("\\newcommand*\\circledblack[1]{\\tikz[baseline=(char.base)]{\\node[shape=circle,draw,inner sep=2pt,fill=black!50] (char) {#1};}}")
    #archivo_salida.write("\\setlength{\\columnsep}{1cm}")
    
   
    archivo_salida.write("\\begin{document}")
    
    for i in range(1,len(prueba)-1): #iterador_pruebas
        archivo_salida.write("\\begin{center}")
        archivo_salida.write("\Large\\textbf{Primera Prueba Global}")
        archivo_salida.write("\\end{center}")
        archivo_salida.write("\\begin{tabular}{ l c r }")
        archivo_salida.write("nombre:  & .....................................\\\\")
        archivo_salida.write("curso :  & .....................................\\\\")
        archivo_salida.write("fecha :  & .....................................\\\\")
        archivo_salida.write("\\end{tabular}")
        
        #archivo_salida.write("\\begin{enumerate}")
        for j in range(0,cantidad_preguntas):
            
            #archivo_salida.write("\\item {0}".format(prueba[str(i)][j]['enunciado']))
            archivo_salida.write("\\subsection*{{{0}.- {1}}}".format(j+1,prueba[str(i)][j]['enunciado']))
            alternativas = json.loads(prueba[str(i)][j]['alternativas_json'])
            archivo_salida.write("\\begin{enumerate}")
            for k in range(0,5):
                archivo_salida.write("\\item {0}".format(alternativas[k]['fields']['texto']))
            archivo_salida.write("\\end{enumerate}")
        #archivo_salida.write("\\end{enumerate}")
        
        archivo_salida.write("\\newpage")        
        archivo_salida.write("\\setcounter{page}{0}")
        archivo_salida.write("\\pagenumbering{arabic}")
        archivo_salida.write("\\setcounter{page}{1}")

    #lo que hay que hacer ahora, es trabajar en el latex para que quede todas las pruebas juntas con su respectivo encabezado
    for i in range(1,len(prueba)-1): #iterador_pruebas
        archivo_salida.write("\Large\\textbf{Primera Prueba Global - Solucionario, no entregar}")
        archivo_salida.write("\\begin{enumerate}")
        for j in range(0,cantidad_preguntas):
            archivo_salida.write("\\item {0}".format(prueba[str(i)][j]['enunciado']))
            archivo_salida.write("{0}".format(prueba[str(i)][j]['explicacion']))
        archivo_salida.write("\\end{enumerate}")
        archivo_salida.write("\\newpage\\setcounter{page}{0}\\setcounter{page}{0}\\setcounter{page}{1}")
    
    # Acá comienza la hoja de respuestas        
    for i in range(1,len(prueba)-1): #iterador_pruebas
        archivo_salida.write("\\begin{center}")
        archivo_salida.write("\Large\\textbf{Primera Prueba Global - Hoja de respuestas}")
        archivo_salida.write("\\end{center}")
        archivo_salida.write("\\begin{tabular}{ l c r }")
        archivo_salida.write("nombre:  & .....................................\\\\")
        archivo_salida.write("curso :  & .....................................\\\\")
        archivo_salida.write("fecha :  & .....................................\\\\")
        archivo_salida.write("\\end{tabular}")

        archivo_salida.write("\\begin{multicols*}{2}")
        archivo_salida.write("\\begin{enumerate}")

        for j in range(0,cantidad_preguntas):
            
            archivo_salida.write("\\item \\circled{a} \\circled{\\begin{small} b \\end{small}} \\circled{c} \\circled{\\begin{small} d \\end{small}} \\circled{e} ")
            
            
            
        archivo_salida.write("\\end{enumerate}")
        archivo_salida.write("\\end{multicols*}")
        archivo_salida.write("\\newpage\\setcounter{page}{0}\\setcounter{page}{0}\\setcounter{page}{1}")
        
    #Acá comienza la hoja de respuestas correctas

    for i in range(1,len(prueba)-1): #iterador_pruebas
        archivo_salida.write("\\Large\\textbf{Plantilla de respuestas correctas}")
        archivo_salida.write("\\begin{multicols*}{2}")
        archivo_salida.write("\\begin{enumerate}")
        for j in range(0,cantidad_preguntas):
            alternativas_2 = json.loads(prueba[str(i)][j]['alternativas_json'])
            texto=""
            for k,l in zip(range(0,5),['a','b','c','d','e']):
                
                if alternativas_2[k]['fields']['es_correcta']==False:
                    texto_formateado = "\\circled{{\\begin{{small}} {} \\end{{small}}}} ".format(l) 
                    texto = texto + texto_formateado
                else:
                    texto_formateado = "\\circledblack{{\\begin{{small}} {} \\end{{small}}}} ".format(l)
                    texto = texto + texto_formateado
            texto_final = "\\item " + texto
            archivo_salida.write(texto_final)
        archivo_salida.write("\\end{enumerate}")
        archivo_salida.write("\\end{multicols*}")
        archivo_salida.write("\\newpage\\setcounter{page}{0}\\setcounter{page}{0}\\setcounter{page}{1}")
    
    archivo_salida.write("\\end{document}")
    archivo_salida.close()
    ejecutable = "pdflatex {0}".format(archivo_salida.name)
    os.system(ejecutable)
    archivo_a_descargar = open("prueba.pdf","rb")# para resolver el error en byte 0 había que abrirlo como binario es decir, usar rb
    respuesta = HttpResponse(archivo_a_descargar,content_type='application/pdf')
    respuesta['Content-Disposition'] = 'attachment; filename="{0}"'.format(archivo_a_descargar.name)
      
    return respuesta
    

def compartir(request):
    formulario_compartir = FormularioCompartir(usuario=request.user)
    tabla_compartidos=CompartirModel.objects.filter(yo=request.user.id)
    
    return render(request,'pruebas/compartir.html',{'formulario_compartir':formulario_compartir,'tabla_compartidos':tabla_compartidos})


from django.core import serializers
def compartir_usurio(request):
    if request.is_ajax():
        resultados=[]
        consulta=request.GET.get("term","")
        otro_usuario=User.objects.filter(username__icontains=consulta).exclude(username__icontains=request.user)
        
        for r in otro_usuario:
            r_jason={}
            r_jason['label']=r.username
            resultados.append(r_jason)
        datos=json.dumps(resultados)
    else:
        datos='no hay nada.'
    return HttpResponse(datos, content_type='application/json')

def guardar_compartidos_vista(request):
    
    if request.method=='POST':
        
        datos_del_formulario = request.POST.copy()
        usuario_a_compartir_id = User.objects.get(username=datos_del_formulario['usuario_a_compartir'])

        data={}
        data['usuario_a_compartir'] = usuario_a_compartir_id.id
        data['tag_a_compartir'] = datos_del_formulario['tag_a_compartir'] 


        fs = FormularioCompartir(data,usuario=request.user)


        if fs.is_valid():

            fs.save(commit=False)
            fs.instance.yo = request.user.id
            #la linea de arriba funciona bien pero no se cómo funciona detrás
            fs.usuario_a_compartir = fs.cleaned_data['usuario_a_compartir']
            fs.tag_a_compartir = fs.cleaned_data['tag_a_compartir']
            fs.save()
            return redirect('compartir') 
            
        
    return HttpResponse('<h1 class="display-1">No se guardó </h1>')

def tabla_compartidos(request):
    tabla_compartidos=CompartirModel.objects.filter(yo=request.user.id)
    return render(request,'pruebas/tabla-compartidos.html',{'tabla_compartidos':tabla_compartidos})

def eliminar_permiso(request):
    i=request.POST.get('id')
    n = CompartirModel.objects.filter(yo=request.user.id,numero_compartido=i)
    n.delete()
    return redirect('compartir')

def eliminar_tag(request,tag_id):
    a = TagModel.objects.get(id_tag=tag_id)
    a.delete()
    return redirect('crear_tag')

def api_traer_tag(request,pregunta_numero):
    """ ESte traería los tag asociados a las preguntas """
    consulta = PreguntaModel.objects.filter(usuario = request.user,unico_pregunta = pregunta_numero).only('tag')
    consulta_json = serializers.serialize('json',consulta)
    return HttpResponse(consulta_json,content_type='application/json')
