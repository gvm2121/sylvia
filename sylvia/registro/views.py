from django.shortcuts import render,redirect
from .formularios import login_form
from registro.models import UsuarioModel
from pruebas.views import index
from django.contrib.auth import login,authenticate
#from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password
#from sylvia.sylviabackend import authenticate

# Create your views here.

def login_sylvia(request):
    formulario_entrada=login_form()
    print('primer registro views login')
    if request.method=='POST':
            formulario_entrada=login_form(request.POST)

            if formulario_entrada.is_valid():
                    
                    nombre=request.POST.get('nombre_login')
                    password=request.POST.get('password_login')
                   
                    user = authenticate(request,username=nombre,password=password)
 
                    
                    if user is not None:
                            
                            print('******',request.user.is_authenticated)
                            login(request,user)
                            
                            print('****** dentro del views',request.user)
                            print('****** dentro del views',request.user.is_authenticated)
                            return redirect('/dentro/inicio')
                    else:
                            print('no autenticado')

                                

    return render(request,'registro/ingreso.html',{'formulario_entrada':formulario_entrada})


def login_inicial(request):
        formulario_entrada=login_form()
        return render(request,'registro/ingreso.html',{'formulario_entrada':formulario_entrada})

