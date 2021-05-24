from django import forms
from datetime import *
from django.forms import SelectDateWidget, TextInput, NumberInput, EmailInput
from .models import marca


class marcaForm(forms.ModelForm):
    # constructor
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        this_year = datetime.now().year
        years = range(this_year - 15, this_year - 3)
        for field in self.Meta.fields:
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })
            self.fields['nombre'].widget = TextInput(
                attrs={'placeholder': 'Ingrese el nombre de la marca',
                       'class': 'form-control form-rounded',
                       'id': 'id_nombre_marca',
                       'autocomplete': 'off'})

        # habilitar, desabilitar, y mas

    class Meta:
        model = marca
        fields = ['nombre',

                  ]
        labels = {
            'nombre': 'Nombre',


        }
        widgets = {
            'nombre': forms.TextInput(),

        }
