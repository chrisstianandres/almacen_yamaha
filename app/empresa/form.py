from django import forms
from datetime import *
from django.forms import SelectDateWidget, TextInput, NumberInput, EmailInput

from .models import empresa


class empresaForm(forms.ModelForm):
    # constructor
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.Meta.fields:
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })

            self.fields['nombre'].widget = TextInput(
                attrs={'placeholder': 'Ingrese el nombre de la Empresa', 'class': 'form-control form-rounded'})
            self.fields['direccion'].widget = TextInput(
                attrs={'placeholder': 'Ingrese numero la direccion de la empresa',
                       'class': 'form-control form-rounded'})
            self.fields['correo'].widget = TextInput(attrs={'placeholder': 'Ingrese correo de la empresa',
                                                            'class': 'form-control form-rounded'})
            self.fields['ciudad'].widget = TextInput(attrs={'placeholder': 'Ingrese la ciudad de la empresa',
                                                            'class': 'form-control form-rounded'})
            self.fields['telefono'].widget = TextInput(
                attrs={'placeholder': 'Ingrese el numero de telefono de la empresa',
                       'class': 'form-control form-rounded'})
            self.fields['iva'].widget = TextInput(attrs={'class': 'form-control form-rounded', 'type': 'number'})
            self.fields['ruc'].widget = TextInput(attrs={'placeholder': 'Ingrese el ruc de la empresa',
                                                         'class': 'form-control form-rounded'})

        # habilitar, desabilitar, y mas

    class Meta:
        model = empresa
        fields = ['nombre',
                  'ciudad',
                  'ruc',
                  'correo',
                  'direccion',
                  'iva',
                  'telefono'
                  ]
        labels = {
            'nombre': 'Nombre',
            'ciudad': 'Ciudad',
            'ruc': 'Ruc',
            'correo': 'Correo',
            'direccion': 'Direecion',
            'iva': 'Iva',
            'telefono': 'Telefono',
        }
        widgets = {
            'nombre': forms.TextInput(),
            'ciudad': forms.TextInput(),
            'ruc': forms.TextInput(),
            'correo': forms.TextInput(),
            'direccion': forms.TextInput(),
            'iva': forms.TextInput(),
            'telefono': forms.TextInput()
        }
