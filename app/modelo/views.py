from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from app.mixin import usuariomixin
from app.modelo.form import modeloForm
from app.modelo.models import modelo
from django.views.generic import *

# Create your views here.
class modelo_list(LoginRequiredMixin,usuariomixin,ListView):
    model = modelo
    template_name = 'modelo/modelo_list.html'

    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                for i in modelo.objects.all():
                    data.append(i.toJSON())
            elif action == 'delete':
                pk = request.POST['id']
                cli = modelo.objects.get(pk=pk)
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
        context['title'] = 'Listado de Modelos'
        context['nuevo'] = reverse_lazy('modelo:crear')
        context['url'] = reverse_lazy('modelo:lista')
        context['entidad'] = 'Modelos'
        return context


class modelo_create(LoginRequiredMixin,usuariomixin,CreateView):
    model = modelo
    form_class = modeloForm
    template_name = 'modelo/modelo_form.html'
    success_url = reverse_lazy('modelo:lista')


    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'add':
                form = self.form_class(request.POST)
                if form.is_valid():
                    form.save()
                else:
                    data['title'] = 'Registro de un Modelo'
                    data['url'] = reverse_lazy('marca:lista')
                    data['entidad'] = 'Modelo'
                    data['action'] = 'add'
                    data['form'] = form
                    return render(request, self.template_name, data)
                return HttpResponseRedirect(self.success_url)
            elif action == 'add_modelo':
                form = self.form_class(request.POST)
                if form.is_valid():
                    pr = form.save()
                    data['modelo'] = pr.toJSON()
                else:
                    data['error'] = form.errors
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Registro de Modelo'
        context['url'] = reverse_lazy('modelo:lista')
        context['entidad'] = 'Modelo'
        context['action'] = 'add'
        return context


class modelo_update(LoginRequiredMixin,usuariomixin,UpdateView):
    model = modelo
    form_class = modeloForm
    template_name = 'modelo/modelo_form.html'
    success_url = reverse_lazy('modelo:lista')

    #@method_decorator(login_required)
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
        context['title'] = 'Edicion de Modelo'
        context['url'] = reverse_lazy('modelo:lista')
        context['entidad'] = 'Modelo'
        context['action'] = 'edit'
        return context


class modelo_delete(LoginRequiredMixin,usuariomixin,DeleteView):
    model = modelo
    form_class = modeloForm
    template_name = 'form_delete.html'
    success_url = reverse_lazy('modelo:lista')

    #@method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Eliminacion de Modelo'
        context['entidad'] = 'Modelo'
        context['url'] = reverse_lazy('modelo:lista')
        context['action'] = 'delete'

        return context
