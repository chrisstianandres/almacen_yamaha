from django.forms import *
from app.ubicacion.models import *


class ubicacionForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['nombre'].widget.attrs['autofocus'] = True

    class Meta:
        model = ubicacion
        fields = ['nombre',
                  'area',
                  'estante']
        widgets = {
            'area': Select(attrs={
                'class': 'form-control select2',
                'sytle': 'with 100%',

            }),

            'estante': Select(attrs={
                'class': 'form-control select2',
                'sytle': 'with 100%',

            }),
            'nombre': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese el nombre del producto',
                'sytle': 'with 100%',

            })
        }
