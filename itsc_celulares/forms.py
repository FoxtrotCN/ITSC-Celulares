from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from django.forms import ModelForm
from django.utils.translation import gettext_lazy as _

from itsc_celulares.models import *


class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "password1", "password2"]
        labels = {
            "username": _("Usuario"),
            "first_name": _("Nombre"),
            "last_name": _("Apellido"),
            "password1": _("Contraseña"),
            "password2": _("Reingresar contraseña"),
        }

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("El usuario ya existe")
        return username

    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')
        if len(password1) < 8:
            raise forms.ValidationError("La contraseña debe contener al menos 8 caracteres y debe ser alfanumerica")
        return password1

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 != password1:
            raise forms.ValidationError("Las contraseñas no coinciden")
        return password1


class CustomerEntryForm(ModelForm):
    class Meta:
        model = Customer
        fields = '__all__'
        labels = {
            "first_name": _("Nombre"),
            "last_name": _("Apellido"),
            "primary_phone_number": _("Número de telefono primario"),
            "secondary_phone_number": _("Número de telefono secundario"),
            "email": _("Correo electrónico"),
        }


class CellPhoneEntryForm(ModelForm):
    class Meta:
        model = CellPhone
        fields = '__all__'
        labels = {
            "brand": _("Marca"),
            "model": _("Modelo"),
            "serial_number": _("Número de serie"),
            "problem_description": _("Descripción del problema"),
            "diagnosis": _("Diagnóstico"),
            "customer": _("Cliente"),
        }


class NewEntryForm(ModelForm):
    class Meta:
        model = RepairOrder
        fields = '__all__'
        labels = {
            "technician": _("Técnico"),
            "device": _("Dispositivo"),
            "order_status": _("Status"),
        }
