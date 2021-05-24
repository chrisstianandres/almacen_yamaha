from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseRedirect, HttpResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
import json
from app.user.form import userForm, GroupForm
from app.user.models import User
from django.views.generic import *
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import Group
from app.mixin import usuariomixin, ValidatePermissionRequiredMixin

# Create your views here.
class user_list(LoginRequiredMixin, usuariomixin, ListView):
    model = User
    template_name = 'user/user_list.html'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                for i in User.objects.all():
                    data.append(i.toJSON())
            elif action == 'delete':
                pk = request.POST['id']
                cli = User.objects.get(pk=pk)
                cli.delete()
                data['resp'] = True
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            print(e)
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Usuarios'
        context['nuevo'] = reverse_lazy('user:crear')
        context['url'] = reverse_lazy('user:lista')
        context['entidad'] = 'Usuarios'
        return context


class user_create(LoginRequiredMixin, usuariomixin, CreateView):
    model = User
    form_class = userForm
    template_name = 'user/user_form.html'
    success_url = reverse_lazy('user:lista')

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'add':
                form = self.get_form()
                data = form.save()
                return HttpResponseRedirect(self.success_url)
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Registro de Usuario'
        context['url'] = reverse_lazy('user:lista')
        context['entidad'] = 'User'
        context['action'] = 'add'
        return context


class user_update(LoginRequiredMixin, usuariomixin, UpdateView):
    model = User
    form_class = userForm
    template_name = 'user/user_form.html'
    success_url = reverse_lazy('user:lista')

    # @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'edit':
                form = self.get_form()
                data = form.save()
                return HttpResponseRedirect(self.success_url)
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edicion de Userio'
        context['url'] = reverse_lazy('user:lista')
        context['entidad'] = 'Usuario'
        context['action'] = 'edit'
        return context


class list_group(LoginRequiredMixin,ValidatePermissionRequiredMixin, ListView):
    model = Group
    template_name = 'group/group_list.html'
    #permission_required = 'user.view_user'

    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'list':
                data = []
                user = Group.objects.all()
                for c in user:
                    data.append({'id': int(c.id), 'nombre': str(c.name),
                                 'permisos': [{'id': p.id, 'nombre': p.name} for p in c.permissions.all()]})
                    print(data)
            elif action == 'delete':
                try:
                    id = request.POST['id']
                    if id:
                        ps = Group.objects.get(pk=id)
                        ps.delete()
                        data['resp'] = True
                    else:
                        data['error'] = 'Ha ocurrido un error'
                except Exception as e:
                    data['error'] = str(e)
            else:
                data['error'] = 'No ha seleccionado una opcion'
        except Exception as e:
            data['error'] = 'No ha seleccionado una opcion'
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['entidad'] = 'Grupos'
        data['title'] = 'Listado de Grupos'
        data['nuevo'] = reverse_lazy('user:crear_grupo')
        data['url'] = reverse_lazy('user:lista_grupo')

        return data

class create_group(LoginRequiredMixin,ValidatePermissionRequiredMixin, CreateView):
    model = Group
    form_class = GroupForm
    template_name = 'group/group_form.html'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST['action']
        try:
            if action == 'add':
                f = GroupForm(request.POST)
                if f.is_valid():
                    f.save()
                    return HttpResponseRedirect('/usuario/groups')
                else:
                    data['form'] = f
                return render(request, 'group/group_form.html', data)
            elif action == 'delete':
                pk = request.POST['id']
                cli = Group.objects.get(pk=pk)
                cli.delete()
                data['resp'] = True
            else:
                data['error'] = 'No ha seleccionado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['entidad'] = 'Grupos'
        data['title'] = 'Nuevo Grupos'
        data['url'] = reverse_lazy('user:lista_grupo')
        data['action'] = 'add'
        return data


class update_group(LoginRequiredMixin,ValidatePermissionRequiredMixin, UpdateView):
    model = Group
    form_class = GroupForm
    template_name = 'group/group_form.html'
    success_url = 'user:groups'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST['action']
        try:
            pk = self.kwargs.get('pk', 0)
            group = self.model.objects.get(id=pk)
            if action == 'edit':
                f = self.form_class(request.POST, request.FILES, instance=group)
                if f.is_valid():
                    f.save()
                    return HttpResponseRedirect('/user/groups')
                else:
                    data = self.get_context_data()
                    data['form'] = f
                return render(request, 'group/group_form.html', data)
            elif action == 'delete':
                pk = request.POST['id']
                cli = Group.objects.get(pk=pk)
                cli.delete()
                data['resp'] = True
            else:
                data['error'] = 'No ha seleccionado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        grupo = self.model.objects.get(id=self.kwargs['pk'])
        data = super().get_context_data(**kwargs)
        data['entidad'] = 'Grupos'
        data['title'] = 'Editar Grupos'
        #data['url'] = '/usuario/newgroup'
        data['form'] = GroupForm(instance=grupo)
        data['action'] = 'edit'

        return data

