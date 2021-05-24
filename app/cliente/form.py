from django import forms
from datetime import *
from django.forms import SelectDateWidget, TextInput, NumberInput, EmailInput
from .models import cliente


class clienteForm(forms.ModelForm):
    # constructor
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        this_year = datetime.now().year
        years = range(this_year - 15, this_year - 3)
        for field in self.Meta.fields:
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })
            self.fields['nombres'].widget = TextInput(
                attrs={'placeholder': 'Ingrese el nombre del cliente', 'class': 'form-control form-rounded',
                       'autocomplete': 'off'})
            self.fields['numero_doc'].widget = TextInput(
                attrs={'placeholder': 'Ingrese numero de documento', 'class': 'form-control form-rounded',
                       'autocomplete': 'off'})
            self.fields['correo'].widget = EmailInput(
                attrs={'placeholder': 'abc@correo.com', 'class': 'form-control form-rounded', 'autocomplete': 'off'})
            self.fields['telefono'].widget.attrs['placeholder'] = 'Ingrese un numero de celular'
            self.fields['direccion'].widget = TextInput(
                attrs={'placeholder': 'Ingrese su direccion con maximo 50 caracteres',
                       'class': 'form-control form-rounded', 'autocomplete': 'off'})

        # habilitar, desabilitar, y mas

    class Meta:
        model = cliente
        fields = ['nombres',
                  'tipo_doc',
                  'numero_doc',
                  'correo',
                  'telefono',
                  'direccion'
                  ]
        labels = {
            'nombres': 'Nombres',
            'tipo_doc': 'Tipo Documento',
            'numero_doc': 'N° de Documento',
            'correo': 'Correo',
            'telefono': 'Celular',
            'direccion': 'Direccion'

        }
        widgets = {
            'nombres': forms.TextInput(),
            'tipo_doc': forms.Select(attrs={'class': 'selectpicker', 'data-width': 'fit'}),
            'numero_doc': forms.TextInput(),
            'correo': forms.EmailInput(),
            'telefono': forms.TextInput(),
            'direccion': forms.TextInput()
        }
        exclude=['fecha']

    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                form.save()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data
