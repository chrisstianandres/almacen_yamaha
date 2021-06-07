from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from app.empleado.form import empleadoForm
from app.empleado.models import empleado
from django.views.generic import *
from app.mixin import usuariomixin

# Create your views here.



class empleado_list(LoginRequiredMixin,usuariomixin,ListView):
    model = empleado
    template_name = 'empleado/empleado_list.html'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                for i in empleado.objects.all():
                    data.append(i.toJSON())
            elif action == 'delete':
                pk = request.POST['id']
                cli = empleado.objects.get(pk=pk)
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
        context['title'] = 'Listado de Empleado'
        context['nuevo'] = reverse_lazy('empleado:crear')
        context['url'] = reverse_lazy('empleado:lista')
        context['entidad'] = 'Empleado'
        return context


class empleado_create(LoginRequiredMixin,usuariomixin,CreateView):
    model = empleado
    form_class = empleadoForm
    template_name = 'empleado/empleado_form.html'
    success_url = reverse_lazy('empleado:lista')

   # @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'add':
                form = self.get_form()
                if form.is_valid():
                    data = form.save()
                else:
                    data['title'] = 'Registro de Empleado'
                    data['url'] = reverse_lazy('empleado:lista')
                    data['entidad'] = 'Empleado'
                    data['action'] = 'add'
                    data['form'] = form
                    return render(request, self.template_name, data)
                return HttpResponseRedirect(self.success_url)
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Registro de Empleado'
        context['url'] = reverse_lazy('empleado:lista')
        context['entidad'] = 'Empleado'
        context['action'] = 'add'
        return context


class empleado_update(LoginRequiredMixin, usuariomixin, UpdateView):
    model = empleado
    form_class = empleadoForm
    template_name = 'empleado/empleado_form.html'
    success_url = reverse_lazy('empleado:lista')

   # @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'edit':
                emp = empleado.objects.get(id=self.kwargs['pk'])
                form = empleadoForm(request.POST, instance=emp)
                if form.is_valid():
                    data = form.save()
                else:
                    data['title'] = 'Registro de Empleado'
                    data['url'] = reverse_lazy('empleado:lista')
                    data['entidad'] = 'Empleado'
                    data['action'] = 'add'
                    data['form'] = form
                    return render(request, self.template_name, data)
                return HttpResponseRedirect(self.success_url)
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            print(e)
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edicion de Empleado'
        context['url'] = reverse_lazy('empleado:lista')
        context['entidad'] = 'Empleado'
        context['action'] = 'edit'
        return context


class empleado_delete(LoginRequiredMixin,usuariomixin,DeleteView):
    model = empleado
    form_class = empleadoForm
    template_name = 'form_delete.html'
    success_url = reverse_lazy('empleado:lista')

    #@method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Eliminacion de Empleado'
        context['entidad'] = 'Empleado'
        context['url'] = reverse_lazy('empleado:lista')

        return context
