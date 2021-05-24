from django.forms import *
from app.empleado.models import *


class empleadoForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['cedula'].widget.attrs['autofocus'] = True

    class Meta:
        model = empleado
        fields = '__all__'
        labels = {'telefono': 'Celular'}
        widgets = {
            'cedula': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese su numero de cedula',
                'sytle': 'with 100%',

            }),
            'nombres': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese su nombres',
                'sytle': 'with 100%',

            }),
            'apellidos': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese sus apellidos',
                'sytle': 'with 100%',

            }),
            'edad': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese su edad',
                'sytle': 'with 100%',

            }),
            'correo': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese su correo',
                'sytle': 'with 100%',

            }),
            'telefono': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese su numero de celular',
                'sytle': 'with 100%',

            }),
            'direccion': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese su direccion',
                'sytle': 'with 100%',

            }),
            'cargo': Select(attrs={
                'class': 'form-control select2',
                'sytle': 'with 100%',

            }),
        }
