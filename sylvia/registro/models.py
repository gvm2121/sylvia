from django.db import models
from django.contrib.auth.models import User


# Create your models here.

#primero hay que cargar todos los RBD de los colegios.
'''

class UsuarioModelManager(BaseUserManager):
    def create_user(self,correo,nombre,password=None):
        if not correo:
            raise ValueError('Debe incluir un email válido')

        user = self.model(
            correo=self.normalize_email(correo),
            nombre=nombre
            
        )

        user.set_password(password)
        user.save(using=self._db)
        return user
    def create_superuser(self, correo,nombre, password):
        user = self.create_user(
            correo,
            nombre=nombre,
            password=password,
            
        )
        user.is_admin = True
        user.save(using=self._db)
        return user
'''
class InstitucionModel(models.Model):
    id_institucion=models.AutoField(primary_key=True)
    institucion=models.TextField()
    rbd=models.IntegerField()
    correo=models.TextField()


class UsuarioModel(models.Model):
    usuario=models.OneToOneField(User, on_delete=models.CASCADE)
    Institucion = models.OneToOneField(InstitucionModel, on_delete=models.CASCADE)


'''

class UsuarioModel(AbstractBaseUser):
    id_usuario=models.AutoField(primary_key=True)
    nombre=models.TextField()
    correo=models.TextField(unique=True)
    objects = UsuarioModelManager()
    REQUIRED_FIELDS = ['nombre']
    USERNAME_FIELD = 'correo'
    EMAIL_FIELD='correo'
    #institucion=models.ForeignKey(InstitucionModel, on_delete=models.CASCADE, null=True, blank=True)
    def __str__(self):
        return self.correo

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin
    @property
    def is_admin(self):
        return True
'''


