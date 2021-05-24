from django import forms
from datetime import *
from django.forms import SelectDateWidget, TextInput, NumberInput, EmailInput
from .models import proveedor
class proveedorForm(forms.ModelForm):
    # constructor
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.Meta.fields:
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })
            self.fields['razon_social'].widget = TextInput(
                attrs={'placeholder': 'Ingrese una razon social', 'class': 'form-control form-rounded',
                       'autocomplete': 'off'})
            self.fields['nombres'].widget = TextInput(
                attrs={'placeholder': 'Ingrese el nombre del proveedor', 'class': 'form-control form-rounded', 'autocomplete': 'off'})
            self.fields['numero_doc'].widget = TextInput(
                attrs={'placeholder': 'Ingrese numero de documento', 'class': 'form-control form-rounded', 'autocomplete': 'off'})
            self.fields['correo'].widget = EmailInput(
                attrs={'placeholder': 'abc@correo.com', 'class': 'form-control form-rounded', 'autocomplete': 'off'})
            self.fields['telefono'].widget.attrs['placeholder'] = 'Ingrese un numero de celular'
            self.fields['direccion'].widget = TextInput(
                attrs={'placeholder': 'Ingrese una direccion con maximo 50 caracteres', 'class': 'form-control form-rounded','autocomplete': 'off'})

        # habilitar, desabilitar, y mas

    class Meta:
        model = proveedor
        fields = ['razon_social',
                  'nombres',
                  'tipo_doc',
                  'numero_doc',
                  'correo',
                  'telefono',
                  'direccion'
                  ]
        labels = {
            'razon_social': 'Razon Social',
            'nombres': 'Nombres',
            'tipo_doc': 'Tipo Documento',
            'numero_doc': 'N° de Documento',
            'correo': 'Correo',
            'telefono': 'Celular',
            'direccion': 'Direccion'

        }
        widgets = {
            'razon_social': forms.TextInput(),
            'nombres': forms.TextInput(),
            'tipo_doc': forms.Select(attrs={'class': 'selectpicker', 'data-width': 'fit'}),
            'numero_doc': forms.TextInput(),
            'correo': forms.EmailInput(),
            'telefono': forms.TextInput(),
            'direccion': forms.TextInput()
        }
