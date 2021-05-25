import json

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.db.models import Count
from django.http import JsonResponse, HttpResponseRedirect, HttpResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from app.cargo.form import cargoForm
from app.cargo.models import cargo
from django.views.generic import *
from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.
from app.mixin import usuariomixin
from app.user.form import GroupForm
from app.user.models import User


class Listgroupsview(ListView):
    model = Group
    template_name = 'rol/cargo_list.html'

    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    # def post(self, request, *args, **kwargs):
    #     data = {}
    #     try:
    #         action = request.POST['action']
    #
    #         # elif action == 'delete':
    #         #     try:
    #         #         id = request.POST['id']
    #         #         if id:
    #         #             ps = User.objects.get(pk=id)
    #         #             ps.delete()
    #         #             data['resp'] = True
    #         #         else:
    #         #             data['error'] = 'Ha ocurrido un error'
    #         #     except Exception as e:
    #         #         data['error'] = str(e)
    #         else:
    #             data['error'] = 'No ha seleccionado una opcion'
    #     except Exception as e:
    #         data['error'] = 'No ha seleccionado una opcion'
    #     return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['icono'] = 'fa fa-user-lock'
        data['entidad'] = 'Cargos'
        data['boton'] = 'Nuevo Cargo'
        data['titulo'] = 'Listado de Cargos'
        data['nuevo'] = '/cargo/crear'
        # data['form'] = UserForm
        return data


class CrudViewGroup(TemplateView):
    form_class = Group
    template_name = 'rol/form.html'

    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST['action']
        try:
            if action == 'modelos':
                data = []
                contentype = ContentType.objects.order_by('model')
                x = 1
                for c in contentype.exclude(model__in=['logentry', 'permission', 'session', 'contenttype', 'cargo',
                                                       'detalle_venta', 'detalle_compra']):
                    nombre = c.model
                    if c.name == 'grupo':
                        nombre = 'rol'
                    data.append({'id': c.id, 'nombre': nombre, 'num': x, 'view': 0, 'add': 0, 'change': 0,
                                 'delete': 0})
                    x += 1
            elif action == 'add':
                datos = json.loads(request.POST['permisos'])
                grupo = Group()
                grupo.name = datos['nombre']
                grupo.save()
                for p in datos['modelos']:
                    if p['add'] == 1:
                        add = '{}_{}'.format('add', p['nombre'])
                        permiso_add = Permission.objects.get(codename=add)
                        grupo.permissions.add(permiso_add.id)
                    if p['view'] == 1:
                        view = '{}_{}'.format('view', p['nombre'])
                        permiso_view = Permission.objects.get(codename=view)
                        grupo.permissions.add(permiso_view.id)
                    if p['change'] == 1:
                        change = '{}_{}'.format('change', p['nombre'])
                        permiso_change = Permission.objects.get(codename=change)
                        grupo.permissions.add(permiso_change.id)
                    if p['delete'] == 1:
                        delete = '{}_{}'.format('delete', p['nombre'])
                        permiso_delete = Permission.objects.get(codename=delete)
                        grupo.permissions.add(permiso_delete.id)
                    grupo.save()
                data['resp'] = True
            else:
                data['error'] = 'No ha seleccionado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['icono'] = 'fa fa-user-lock'
        data['entidad'] = 'Roles'
        data['boton'] = 'Guardar Rol'
        data['titulo'] = 'Nuevo Rol'
        data['nuevo'] = reverse_lazy('rol/nuevo')
        data['form'] = GroupForm
        data['option'] = 'modelos'
        data['title'] = 'Listado de Roles'
        data['url'] = reverse_lazy('cargo:lista')
        return data


class UpdateViewGroup(UpdateView):
    form_class = GroupForm
    model = Group
    template_name = 'rol/form.html'

    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST['action']
        try:

            if action == 'editar':
                data = []
                pk = self.kwargs['pk']
                contentype = ContentType.objects.all().order_by('model')
                x = 1
                for c in contentype.exclude(model__in=['logentry', 'permission', 'session', 'contenttype', 'cargo',
                                                       'detalle_venta', 'detalle_compra']):
                    nombre = c.model
                    set_add = 0
                    set_view = 0
                    set_delete = 0
                    set_change = 0
                    if c.name == 'grupo':
                        nombre = 'group'
                    add = '{}_{}'.format('add', nombre)
                    view = '{}_{}'.format('view', nombre)
                    change = '{}_{}'.format('change', nombre)
                    delete = '{}_{}'.format('delete', nombre)
                    if Group.objects.filter(permissions__codename=add, id=pk):
                        set_add = 1
                    if Group.objects.filter(permissions__codename=view, id=pk):
                        set_view = 1
                    if Group.objects.filter(permissions__codename=change, id=pk):
                        set_change = 1
                    if Group.objects.filter(permissions__codename=delete, id=pk):
                        set_delete = 1
                    if c.name == 'grupo':
                        nombre = 'cargo'
                    data.append({'id': c.id, 'nombre': nombre, 'num': x, 'view': set_view, 'add': set_add,
                                 'change': set_change, 'delete': set_delete})

                    x += 1
            elif action == 'add':
                datos = json.loads(request.POST['permisos'])
                grupo = Group.objects.get(id=self.kwargs['pk'])
                grupo.permissions.clear()
                grupo.name = datos['nombre']
                grupo.save()
                for p in datos['modelos']:
                    if p['nombre'] == 'cargo':
                        p['nombre'] = 'group'
                    if p['add'] == 1:
                        add = '{}_{}'.format('add', p['nombre'])
                        permiso_add = Permission.objects.get(codename=add)
                        grupo.permissions.add(permiso_add.id)
                    if p['view'] == 1:
                        view = '{}_{}'.format('view', p['nombre'])
                        permiso_view = Permission.objects.get(codename=view)
                        grupo.permissions.add(permiso_view.id)
                    if p['change'] == 1:
                        change = '{}_{}'.format('change', p['nombre'])
                        permiso_change = Permission.objects.get(codename=change)
                        grupo.permissions.add(permiso_change.id)
                    if p['delete'] == 1:
                        delete = '{}_{}'.format('delete', p['nombre'])
                        permiso_delete = Permission.objects.get(codename=delete)
                        grupo.permissions.add(permiso_delete.id)
                    grupo.save()
                data['resp'] = True
            else:
                data['error'] = 'No ha seleccionado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        dato = self.model.objects.get(pk=self.kwargs['pk'])
        data['icono'] = 'fa fa-user-lock'
        data['entidad'] = 'Rol'
        data['boton'] = 'Guardar Rol'
        data['titulo'] = 'Nuevo Rol'
        data['nuevo'] = 'rol/nuevo'
        data['form'] = GroupForm(instance=dato)
        data['option'] = 'editar'
        return data


class DeleteViewGroup(DeleteView):
    model = Group
    template_name = 'rol/form.html'

    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST['action']
        try:
            if action == 'delete':
                id = self.kwargs['pk']
                grupo = Group.objects.get(id=id)
                if User.objects.filter(groups__exact=grupo):
                    data['error'] = 'Este rol esta asignado a uno o mas usuarios'
                else:
                    grupo.delete()
                    data['resp'] = True
            else:
                data['error'] = 'No ha seleccionado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        dato = self.model.objects.get(pk=self.kwargs['pk'])
        data['icono'] = 'fa fa-user-lock'
        data['entidad'] = 'Cargo'
        data['boton'] = 'Guardar Rol'
        data['titulo'] = 'Nuevo Rol'
        data['nuevo'] = 'rol/nuevo'
        data['form'] = GroupForm(instance=dato)
        data['option'] = 'editar'
        return data
