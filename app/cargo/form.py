from django import forms
from datetime import *
from django.forms import SelectDateWidget, TextInput, NumberInput, EmailInput
from .models import cargo

class cargoForm(forms.ModelForm):
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
                attrs={'placeholder': 'Ingrese el nombre del cargo', 'class': 'form-control form-rounded','autocomplete': 'off'})
            self.fields['sueldo'].widget = TextInput(
                attrs={'placeholder': 'Ingrese el sueldo del cargo', 'class': 'form-control form-rounded','autocomplete': 'off'})

        # habilitar, desabilitar, y mas

    class Meta:
        model = cargo
        fields = ['nombre',
                  'sueldo'
                  ]
        labels = {
            'nombre': 'Nombre',
            'sueldo': 'Sueldo'

        }
        widgets = {
            'nombre': forms.TextInput(),
            'sueldo': forms.TextInput(),
        }
