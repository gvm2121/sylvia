from django.forms import ModelForm
from django import forms
from django.forms import ModelForm,Textarea,TextInput,PasswordInput,EmailInput

class login_form(forms.Form):
    nombre_login=forms.CharField()
    password_login=forms.CharField()
    widget ={
        nombre_login : Textarea(attrs={'class':'form-control'})


    }
