from django.forms import *
from app.gasto.models import *


class gastoForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['tipo_gasto'].widget.attrs['autofocus'] = True

    class Meta:
        model = gasto
        fields = '__all__'
        widgets = {
            'tipo_gasto': Select(attrs={
                'class': 'form-control select2',
                'sytle': 'with 100%',

            }),
            'fecha': DateInput(format='%Y-%m-%d',
                                     attrs={
                                         'autocomplete': 'off',
                                         'class': 'form-control datetimepicker-input',
                                         'value': datetime.now().strftime('%Y-%m-%d'),
                                         'id': 'fecha',
                                         'data-target': '#fecha',
                                         'data-toggle': 'datetimepicker'
                                     }),

            'valor': TextInput(attrs={
                'class': 'form-control',
                'type': 'number',
                'value': '1.00',
                'min': "1.00",
                'max': "10000.00",
                'step': "0.01",
                'placeholder': 'Ingrese el valor del gasto',
                'sytle': 'with 100%',

            }),
            'detalle': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese un detalle del gasto',
                'sytle': 'with 100%',

            }),
        }
