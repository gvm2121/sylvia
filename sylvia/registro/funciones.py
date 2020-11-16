from .models import UsuarioModel

def esta_autenticado(email,password):
    if UsuarioModel.objects.filter(correo=email,password=password):
        return True
    else:
        return False

