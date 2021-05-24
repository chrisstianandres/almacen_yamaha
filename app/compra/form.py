from django.forms import *
from app.compra.models import *

class compraForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['proveedor'].widget.attrs['autofocus'] = True
        self.fields['proveedor'].queryset = proveedor.objects.none()

    class Meta:
        model = compra
        fields = '__all__'
        widgets = {
            'proveedor': Select(attrs={
                'class': 'custon_select select2',
                #'sytle': 'with 100%',

            }),
            'fecha_compra': DateInput(format='%Y-%m-%d',
                                     attrs={
                                         'autocomplete': 'off',
                                         'readonly': True,
                                         'class': 'form-control datetimepicker-input',
                                         'value': datetime.now().strftime('%Y-%m-%d'),
                                         'id': 'fecha_compra',
                                         'data-target': '#fecha_compra',
                                         'data-toggle': 'datetimepicker'
                                            }),


            'comprobante': TextInput(attrs={
                'placeholder': 'N° de Comprobante',
                'class': 'form-control',
                'sytle': 'with 100%',

            }),
            'total': TextInput(attrs={
                'readonly': True,
                'class': 'form-control',
                'sytle': 'with 100%',

            }),
            'estado': Select(attrs={
                'class': 'form-control select2',
                'sytle': 'with 100%',

            }),
        }
