from django.contrib.auth.models import Group
from django.forms import *
from app.user.models import *
from django import forms


class userForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs['autofocus'] = True

    class Meta:
        model = User
        fields = [
            'cedula',
            'first_name',
            'last_name',
            'username',
            'password',
            'email',
            'telefono',
            'foto',
            'direccion',
            'sexo',
            'groups',
            'is_superuser'
        ]
        labels = {
            'cedula': 'Cedula',
            'first_name': 'Nombres',
            'last_name': 'Apellidos',
            'username': 'Nombre de Usuario',
            'password': 'Contraseña',
            'email': 'Correo Electronico',
            'telefono': 'Telefono',
            'direccion': 'Direccion',
            'sexo': 'Genero',
            'foto': 'Foto',
            'groups': 'Rol',
            'is_superuser': 'Administraidor (Super Usuario)'

        }
        widgets = {
            'cedula': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese su numero de cedula',
                'sytle': 'with 100%',

            }),
            'first_name': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese sus nombres',
                'sytle': 'with 100%',

            }),
            'last_name': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese su apellidos',
                'sytle': 'with 100%',

            }),
            'username': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese su nombre de usuario',
                'sytle': 'with 100%',

            }),
            'password': PasswordInput(render_value=True,
                                      attrs={
                                          'class': 'form-control',
                                          'placeholder': 'Ingrese su password',
                                          'sytle': 'with 100%',

                                      }),
            'email': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese su correo',
                'sytle': 'with 100%',

            }),
            'telefono': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese su numero de telefono',
                'sytle': 'with 100%',

            }),
            'direccion': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese su direccion',
                'sytle': 'with 100%',

            }),
            'sexo': Select(attrs={
                'class': 'form-control select2',
                'sytle': 'with 100%',

            }),
            'groups': SelectMultiple(attrs={
                'class': 'form-control select2',
                'sytle': 'with 100%',
                'multiple': 'multiple'
            })
        }
        exclude = ['user_permissions', 'last_login', 'date_joined']

    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                pwd = self.cleaned_data['password']
                u = form.save(commit=False)
                if u.pk is None:
                    u.set_password(pwd)
                else:
                    user = User.objects.get(pk=u.pk)
                    if user.password != pwd:
                        u.set_password(pwd)
                u.save()
                u.groups.clear()
                for g in self.cleaned_data['groups']:
                    u.groups.add(g)
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data


class GroupForm(forms.ModelForm):
    # constructor
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.Meta.fields:
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })
            self.fields['name'].widget.attrs = {
                'class': 'form-control form-control-sm input-sm'}
            self.fields['permissions'].widget.attrs = {
                'class': 'form-control form-control-sm input-sm select2', 'multiple': 'multiple'}

    class Meta:
        model = Group
        fields = ['name', 'permissions']
        labels = {'name': 'Nombre', 'permissions': 'Permisos'}
        widgets = {'name': forms.TextInput()}