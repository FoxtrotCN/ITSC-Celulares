from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
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


class CustomerEntryForm(ModelForm):
    class Meta:
        model = Customer
        fields = '__all__'


class CellPhoneEntryForm(ModelForm):
    class Meta:
        model = CellPhone
        fields = '__all__'


class NewEntryForm(ModelForm):
    class Meta:
        model = RepairOrder
        fields = '__all__'
