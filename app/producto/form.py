from django.forms import *
from app.producto.models import *


class productoForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['nombre'].widget.attrs['autofocus'] = True

    class Meta:
        model = producto
        exclude = ['stock']
        fields = ['nombre',
                  'marca',
                  'modelo',
                  'descripcion',
                  'pvp',
                  'p_venta',
                  'imagen'

                  ]
        labels = {
            'pvp': 'Precio de compra',
            'p_venta': 'Precio de venta',
        }
        widgets = {
            'marca': Select(attrs={
                'class': 'form-control select2',
                'sytle': 'with 100%',

            }),

            'modelo': Select(attrs={
                'class': 'form-control select2',
                'sytle': 'with 100%',

            }),
            'nombre': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese el nombre del producto',
                'sytle': 'with 100%',
                'id': 'id_nombre_producto'

            }),
            'descripcion': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese una descripcion al producto',
                'sytle': 'with 100%',

            }),
            'pvp': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese el valor de compra del producto',
                'sytle': 'with 100%',
                'type': 'number',
                'step': "0.01",

            }),
            'p_venta': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese el valor de venta del producto',
                'sytle': 'with 100%',
                'type': 'number',
                'step': "0.01",

            }),
        }
